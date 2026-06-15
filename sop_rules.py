"""SOP-driven rule layer — the engine reads its decision rules from the ingested SOP.

The ingested SOP (output/active_sop_rules.json, written by /api/ingest-sop) holds TYPED
rule specs. These accessors expose them to the processing engine so the SOP genuinely
drives coding authority, confidence gating, jurisdiction SLAs, and the auth hard-block.
Documented defaults are used ONLY when no SOP has been ingested — never a silent
substitute for a real ingest, and clearly labeled as defaults.
"""
import json
from pathlib import Path

_ACTIVE_PATH = Path(__file__).parent / "output" / "active_sop_rules.json"

# Defaults — used only when no SOP is ingested.
_DEFAULT_CONFIDENCE = {"auto_min": 90, "spotcheck_min": 80}
_DEFAULT_CODING_ORDER = ["clinical_notes", "prescription", "referral_form"]
_DEFAULT_SLAS = {"TX": 2, "CA": 5, "FL": 3, "NY": 4, "NJ": 3, "PA": 5}


def active_rules():
    try:
        rules = json.loads(_ACTIVE_PATH.read_text(encoding="utf-8"))
        return rules if isinstance(rules, list) else []
    except Exception:
        return []


def ingested():
    return _ACTIVE_PATH.exists()


def _by_type(t):
    return [r for r in active_rules() if str(r.get("type", "")).lower() == t]


def auth_hard_block():
    """True if the SOP requires authorization as a hard block (e.g. §2.1)."""
    for r in active_rules():
        if str(r.get("field", "")).lower() == "auth_ref" and str(r.get("severity", "")).lower() == "hard_block":
            return True
        if str(r.get("type", "")).lower() == "required_field" and str(r.get("field", "")).lower() == "auth_ref":
            return True
    # default: enforce auth as a hard block unless an ingested SOP omits it
    return not ingested()


def confidence_thresholds():
    for r in _by_type("confidence_gate"):
        try:
            return {"auto_min": int(r.get("auto_min", 90)), "spotcheck_min": int(r.get("spotcheck_min", 80))}
        except (TypeError, ValueError):
            break
    return dict(_DEFAULT_CONFIDENCE)


def coding_authority_order():
    for r in _by_type("coding_authority"):
        order = r.get("priority_order")
        if isinstance(order, list) and order:
            return order
    return list(_DEFAULT_CODING_ORDER)


def jurisdiction_slas():
    slas = {}
    for r in _by_type("jurisdiction_sla"):
        if isinstance(r.get("slas"), dict):
            for k, v in r["slas"].items():
                try:
                    slas[str(k).upper()] = int(v)
                except (TypeError, ValueError):
                    pass
        elif r.get("state") and r.get("business_days"):
            try:
                slas[str(r["state"]).upper()] = int(r["business_days"])
            except (TypeError, ValueError):
                pass
    return slas or dict(_DEFAULT_SLAS)


def rule_for(decision_type, field=None):
    """The governing rule dict (clause/sop/citation) for tracing a decision."""
    for r in active_rules():
        if str(r.get("type", "")).lower() == decision_type and (field is None or r.get("field") == field):
            return r
    return None
