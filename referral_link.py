"""
Parking Lot 1 — Fax / supplemental-document linking.

When a new fax (or referral) is processed, decide whether it belongs to an
EXISTING open referral instead of creating a duplicate. Match primarily on the
claim number (normalized), with a fallback to patient name + DOB. If matched,
merge the new fields into the existing episode — supplemental documents fill the
prior gaps (e.g., a follow-up fax that supplies the missing authorization).
"""
import json
import re
from pathlib import Path


def _norm(s) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def find_open_episode(output_dir, claim_number, patient_name="", dob="", exclude_claim=""):
    """Search saved episode sidecars for an OPEN (incomplete) episode that matches.

    Returns {claim, fields, completeness, path} or None. Only episodes that still
    have gaps are candidates — a complete episode isn't waiting on supplements.
    """
    cn = _norm(claim_number)
    pid = _norm(patient_name) + "|" + _norm(dob)
    for p in sorted(Path(output_dir).glob("fields-*.json"),
                    key=lambda x: x.stat().st_mtime, reverse=True):
        if exclude_claim and exclude_claim in p.name:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        f = data.get("fields", {}) or {}
        comp = data.get("completeness", {}) or {}
        if comp.get("is_complete", True):
            continue  # already complete — not awaiting a supplement
        ecn = _norm(f.get("claim_number"))
        epid = _norm(f.get("patient_name")) + "|" + _norm(f.get("dob"))
        matched = (cn and ecn and cn == ecn) or (pid != "|" and pid == epid)
        if matched:
            return {"claim": f.get("claim_number") or p.stem,
                    "fields": f, "completeness": comp, "path": str(p)}
    return None


def merge_fields(existing: dict, incoming: dict) -> dict:
    """Supplemental fills blanks: keep existing non-empty values, fill empty ones
    from the incoming document."""
    merged = dict(existing or {})
    for k, v in (incoming or {}).items():
        if v not in (None, "", []) and not str(merged.get(k, "")).strip():
            merged[k] = v
    return merged


def resolved_gaps(old_comp: dict, new_comp: dict) -> list:
    """Which gaps the supplemental closed."""
    old = set((old_comp or {}).get("gaps", {}).keys())
    new = set((new_comp or {}).get("gaps", {}).keys())
    return sorted(old - new)
