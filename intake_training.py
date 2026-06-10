"""
Intaketraining — Coached Intake Simulator.

Curated training cases plus a grader that coaches the trainee the same way the
production agent decides: cross-reference documents, validate ICD against CMS
rules, classify gaps by criticality, and escalate rather than guess.

Each case asks the trainee four things — primary ICD, is-there-a-conflict,
blocking gaps, and the route/request-info/escalate decision — then grades each
dimension and returns coaching with the specific CMS citation.
"""

DECISIONS = {
    "route": "Route — dispatch the clean episode",
    "request_info": "Request info — hold and chase the gap (outreach)",
    "escalate": "Escalate — send to a clinical/coding specialist",
}

GAP_OPTIONS = ["auth_ref", "appt_window", "transportation", "language", "none"]

CASES = [
    {
        "id": "post_surgical_miscode",
        "level": 1,
        "title": "The Post-Surgical Miscode",
        "patient": "James Holloway",
        "summary": "Workers' comp referral, s/p ACL reconstruction. DME requested: E0143 rollator walker. Carrier: Pacific Mutual.",
        "documents": [
            {"name": "Referral form", "facts": ["Primary Dx: M23.611 (derangement of medial meniscus)", "DME: E0143 four-wheel rollator", "Auth ref: AUTH-2026-0412", "Appt window: provided"]},
            {"name": "Clinical / op notes", "facts": ["s/p ACL reconstruction, surgery 03/28/2026", "Diagnosis: S83.209A (tear of unspecified meniscus, initial)", "Patient weight: 208 lbs"]},
            {"name": "Prescription", "facts": ["E0143 rollator walker", "Post-surgical mobility support"]},
        ],
        "answer": {"icd": "S83.209A", "has_conflict": True, "blocking_gaps": ["none"], "decision": "escalate"},
        "coaching": {
            "icd": {"rule": "DME-ICD-001 · ICD-10-CM §I.C.19.a", "why": "After a surgical procedure, code the injury (S-code), not the degenerative condition (M-code). M23.611 is degenerative; the op note confirms a traumatic ACL repair → S83.209A is correct."},
            "conflict": {"rule": "Document cross-reference", "why": "The referral form (M23.611) and the clinical notes (S83.209A) disagree. Always cross-check documents — never take the referral form at face value."},
            "gaps": {"rule": "Completeness check", "why": "Auth ref and appointment window are both present, so there is no blocking gap here — the issue is the coding conflict, not a missing field."},
            "decision": {"rule": "Confidence gate (<80%)", "why": "Two source documents conflict on a clinical code → escalate to a specialist rather than guess. This is exactly the judgment the agent leaves to a human."},
        },
    },
    {
        "id": "missing_authorization",
        "level": 1,
        "title": "The Missing Authorization",
        "patient": "Maria Delgado",
        "summary": "Workers' comp referral for a lumbar back brace following a work injury. DME requested: L0631 (TLSO). Carrier: Liberty Mutual.",
        "documents": [
            {"name": "Referral form", "facts": ["Primary Dx: S33.5XXA (sprain of lumbar spine, initial)", "DME: L0631 (TLSO back brace)", "Auth ref: (blank)", "Appt window: provided"]},
            {"name": "Clinical notes", "facts": ["Lumbar strain, work injury 05/14/2026", "Dx consistent: S33.5XXA", "Patient weight: 165 lbs"]},
            {"name": "Prescription", "facts": ["L0631 TLSO", "6-week wear schedule"]},
        ],
        "answer": {"icd": "S33.5XXA", "has_conflict": False, "blocking_gaps": ["auth_ref"], "decision": "request_info"},
        "coaching": {
            "icd": {"rule": "DME-ICD-024 · §I.C.19", "why": "S33.5XXA is correct and consistent across documents — a traumatic injury code for a work-related lumbar sprain."},
            "conflict": {"rule": "Document cross-reference", "why": "The documents agree on the diagnosis — there is no coding conflict in this case."},
            "gaps": {"rule": "DME-ICD-015 · Prior-auth requirement", "why": "The authorization reference is blank. On a WC claim this is a HARD BLOCK — the claim cannot be billed without it. Appointment window is present, so auth_ref is the only blocker."},
            "decision": {"rule": "Completeness — hard block", "why": "Don't dispatch and don't escalate — request the missing auth from the adjuster (outreach). The episode is held until it's resolved."},
        },
    },
    {
        "id": "bariatric_trap",
        "level": 2,
        "title": "The Bariatric Trap",
        "patient": "Robert Pierce",
        "summary": "Workers' comp referral, s/p ACL reconstruction. DME requested: E0143 rollator walker. Everything looks clean — codes match, auth present. Look closely.",
        "documents": [
            {"name": "Referral form", "facts": ["Primary Dx: S83.209A (initial)", "DME: E0143 rollator (standard, 300 lb capacity)", "Auth ref: AUTH-2026-0588", "Appt window: provided"]},
            {"name": "Clinical notes", "facts": ["s/p ACL reconstruction 04/02/2026", "Dx: S83.209A — consistent", "Patient weight: 285 lbs"]},
            {"name": "Prescription", "facts": ["E0143 rollator walker"]},
        ],
        "answer": {"icd": "S83.209A", "has_conflict": False, "blocking_gaps": ["none"], "decision": "request_info"},
        "coaching": {
            "icd": {"rule": "DME-ICD-002 · §I.C.19.a", "why": "S83.209A is correct and consistent — no coding issue here."},
            "conflict": {"rule": "Document cross-reference", "why": "Documents agree — no conflict. This case is designed to look clean."},
            "gaps": {"rule": "Completeness check", "why": "Auth and appointment window are present — no standard field is missing. The trap isn't a missing field."},
            "decision": {"rule": "DME-ICD-008 / 023 · CMS LCD L33803", "why": "The catch: the patient is 285 lbs and the E0143 rollator is rated to 300 lbs — within 15 lbs of the limit. Confirm a bariatric E0149 (400 lb) before dispatch, or you ship the wrong equipment and trigger a costly return. A rushed associate routes this clean; the expert flags it."},
        },
    },
]

_CASE_BY_ID = {c["id"]: c for c in CASES}


def list_cases():
    """Public case list (no answer keys leaked to the client)."""
    out = []
    for c in CASES:
        out.append({k: c[k] for k in ("id", "level", "title", "patient", "summary", "documents")})
    return {"cases": out, "decisions": DECISIONS, "gap_options": GAP_OPTIONS}


def _norm(s):
    return str(s or "").strip().upper().replace(" ", "")


def grade(case_id, sub):
    """Grade a trainee submission against the case answer key, with coaching."""
    case = _CASE_BY_ID.get(case_id)
    if not case:
        return {"error": "unknown case"}
    a = case["answer"]
    co = case["coaching"]

    your_gaps = sub.get("blocking_gaps") or []
    if isinstance(your_gaps, str):
        your_gaps = [your_gaps]
    your_gaps = [g for g in your_gaps if g] or ["none"]

    items = []
    def add(dim, correct, your, expected):
        items.append({"dim": dim, "correct": bool(correct), "your": your,
                      "expected": expected, "rule": co[dim]["rule"], "why": co[dim]["why"]})

    add("icd", _norm(sub.get("icd")) == _norm(a["icd"]), sub.get("icd", ""), a["icd"])
    add("conflict", bool(sub.get("has_conflict")) == a["has_conflict"],
        "Yes" if sub.get("has_conflict") else "No", "Yes" if a["has_conflict"] else "No")
    add("gaps", set(map(str.lower, your_gaps)) == set(a["blocking_gaps"]),
        ", ".join(your_gaps), ", ".join(a["blocking_gaps"]))
    add("decision", sub.get("decision") == a["decision"],
        DECISIONS.get(sub.get("decision", ""), sub.get("decision", "—")), DECISIONS[a["decision"]])

    score = sum(1 for i in items if i["correct"])
    return {"case_id": case_id, "title": case["title"], "score": score, "max": len(items),
            "passed": score >= 3, "items": items}
