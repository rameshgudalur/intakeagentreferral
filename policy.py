"""
Parking Lot 4 — Jurisdiction constraints & SLAs.
Parking Lot 9 — Confidence-tiered autonomy.

WC is state-regulated, so turnaround SLAs vary by jurisdiction. And the agent's
autonomy should be tiered by its confidence. Both are config-driven here so a
client's actual rules/thresholds can be dropped in.
"""
import re

# ── Parking Lot 4: jurisdiction turnaround SLAs (business days) ───────────────
JURISDICTION_SLA = {
    "TX": {"days": 2, "note": "Texas DWC — expedited turnaround"},
    "CA": {"days": 5, "note": "California DWC"},
    "FL": {"days": 3, "note": "Florida DWC"},
    "NY": {"days": 4, "note": "New York WCB"},
    "NJ": {"days": 3, "note": "New Jersey WC"},
    "PA": {"days": 5, "note": "Pennsylvania WC"},
}
_DEFAULT_SLA = {"days": 5, "note": "Standard turnaround"}
_STATE_RE = re.compile(r",\s*([A-Z]{2})\s+\d{5}")


def detect_state(fields: dict) -> str:
    """Pull the 2-letter state from the delivery address (…, ST 12345)."""
    m = _STATE_RE.search(str(fields.get("delivery_address", "")))
    return m.group(1) if m else ""


def assess_jurisdiction(fields: dict) -> dict:
    state = detect_state(fields)
    sla = JURISDICTION_SLA.get(state, _DEFAULT_SLA)
    priority = "HIGH" if sla["days"] <= 2 else ("MED" if sla["days"] <= 3 else "STD")
    return {"state": state or "—", "sla_days": sla["days"],
            "note": sla["note"], "sla_priority": priority}


# ── Parking Lot 9: confidence-tiered autonomy ─────────────────────────────────
# Thresholds configurable to the client's risk tolerance.
TIER_HIGH = 90   # >= → fully autonomous (auto-route)
TIER_MED = 80    # >= → act but flag for human spot-check; < → escalate

def confidence_tier(conf) -> dict:
    try:
        c = float(conf)
    except (TypeError, ValueError):
        return {"tier": "UNKNOWN", "autonomy": "review", "label": "needs review"}
    if c >= TIER_HIGH:
        return {"tier": "HIGH", "autonomy": "autonomous", "label": "auto-route"}
    if c >= TIER_MED:
        return {"tier": "MEDIUM", "autonomy": "spot-check", "label": "act + human spot-check"}
    return {"tier": "LOW", "autonomy": "escalate", "label": "escalate to specialist"}
