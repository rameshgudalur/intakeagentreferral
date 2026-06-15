"""Autonomous RPA delivery — drives the legacy intake UI to file the agent's record.

This is REAL browser automation (Playwright/Chromium), not a simulation. It is the
'last mile' for clients whose legacy systems have no usable API: the bot operates the
application's screen the way a person would. It is *autonomous* in that it reads the
target form's own field labels from the live DOM and maps the agent's structured record
to them — so it adapts to the form rather than relying on hardcoded coordinates.

In deployment the same engine is pointed at the client's actual application; here it is
pointed at a faithful stand-in (the MediClaim Legacy Intake mock) served by this app.

Uses the ASYNC Playwright API (asyncio, no greenlet dependency) so it runs cleanly inside
a Flask request thread and in locked-down / headless environments.
"""
import asyncio
import base64

# Map a legacy field's human label (lowercased) -> the agent record key that feeds it.
# Keyword-based so it adapts to label wording, not a fixed selector list.
_LABEL_RULES = [
    # order matters: 'claimant'/'name' is checked before 'claim' (else "Claimant Name"
    # would match the 'claim' substring and grab the claim number).
    (("claimant", "patient", "name"),         "patient_name"),
    (("file no", "claim"),                    "claim_number"),
    (("birth", "dob"),                        "dob"),
    (("carrier", "insurance"),                "insurance_carrier"),
    (("auth",),                               "auth_ref"),
    (("hcpcs", "procedure code"),             "hcpcs"),
    (("diagnosis", "icd"),                    "icd_code"),
    (("equipment", "service", "dme"),         "dme_item"),
    (("qty", "quantity"),                     "quantity"),
    (("address", "delivery"),                 "delivery_address"),
    (("npi",),                                "physician_npi"),
    (("provider", "physician", "referring"),  "physician_name"),
]


def _value_for(label, record):
    """Pick the record value for a field given its label text (adaptive mapping)."""
    t = (label or "").lower()
    if "npi" in t:                                  # NPI must win over the generic provider rule
        return "physician_npi", record.get("physician_npi", "")
    for keywords, key in _LABEL_RULES:
        if any(k in t for k in keywords):
            return key, record.get(key, "")
    return None, ""


async def _label_for_input(handle):
    try:
        txt = await handle.evaluate(
            """el => {
                const row = el.closest('tr');
                if (row) { const lab = row.querySelector('td'); if (lab) return lab.innerText; }
                return el.getAttribute('aria-label') || el.getAttribute('name') || '';
            }"""
        )
        return (txt or "").strip()
    except Exception:
        return ""


async def _shot(page, label):
    png = await page.screenshot(type="png")
    return {"label": label, "img": "data:image/png;base64," + base64.b64encode(png).decode("ascii")}


async def _deliver_async(base_url, record, slow_mo):
    from playwright.async_api import async_playwright

    steps, shots = [], []
    confirmation, filled = None, 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=slow_mo)
        page = await browser.new_page(viewport={"width": 800, "height": 900})
        try:
            await page.goto(base_url + "legacy-intake", wait_until="networkidle", timeout=20000)
            steps.append("Opened MediClaim Legacy Intake System v4.2 (no API — keyed entry)")
            shots.append(await _shot(page, "Legacy system opened"))

            # Discover the form's fields from the live DOM, then map our record to them.
            handles = await page.query_selector_all("form#intake-form input[name]")
            inputs = []
            for h in handles:
                t = await h.get_attribute("type")
                if (t or "text") not in ("hidden", "submit", "reset"):
                    inputs.append(h)
            steps.append(f"Bot read {len(inputs)} fields off the legacy screen and mapped them to the agent's record")

            for h in inputs:
                label = await _label_for_input(h)
                key, value = _value_for(label, record)
                # Adapt to the legacy field's expected format: "Last, First" name entry.
                if key == "patient_name" and value and "," not in value and "last, first" in label.lower():
                    parts = str(value).split()
                    if len(parts) >= 2:
                        value = parts[-1] + ", " + " ".join(parts[:-1])
                if key == "auth_ref" and not value:
                    value = "PENDING — held per SOP §2.1"     # the SOP decision carries through
                if not value:
                    continue
                await h.scroll_into_view_if_needed()
                await h.fill(str(value))
                filled += 1
                steps.append(f"Keyed  {label.rstrip(':')}  =  {value}")

            shots.append(await _shot(page, f"{filled} fields entered by the bot"))

            await page.click("#submit")
            await page.wait_for_selector("#conf-number", timeout=15000)
            confirmation = (await page.inner_text("#conf-number")).strip()
            steps.append(f"Submitted — legacy system accepted the record and returned {confirmation}")
            shots.append(await _shot(page, "Filed to system of record"))
        finally:
            await browser.close()

    return {"ok": True, "confirmation": confirmation, "fields_filled": filled,
            "steps": steps, "screenshots": shots}


def deliver(base_url, record, slow_mo=70):
    """Drive the legacy intake screen and file the record. Returns steps + screenshots +
    confirmation. Raises if Playwright/Chromium is unavailable (caller surfaces that)."""
    if not base_url.endswith("/"):
        base_url += "/"
    return asyncio.run(_deliver_async(base_url, record, slow_mo))
