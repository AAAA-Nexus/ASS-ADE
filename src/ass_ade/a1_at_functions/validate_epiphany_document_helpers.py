"""Tier a1 — assimilated function 'validate_epiphany_document'

Assimilated from: rebuild/epiphany_cycle.py:170-187
"""

from __future__ import annotations


# --- assimilated symbol ---
def validate_epiphany_document(doc: object) -> list[str]:
    """Return human-readable errors; empty list means OK."""
    errs: list[str] = []
    if not isinstance(doc, dict):
        return ["document must be a JSON object"]
    if doc.get("schema_version") != SCHEMA_VERSION:
        errs.append("schema_version mismatch")
    if not str(doc.get("goal", "")).strip():
        errs.append("goal is required")
    for key in ("epiphanies", "hypotheses", "experiments", "promotion_checks", "plan_steps"):
        val = doc.get(key)
        if not isinstance(val, list) or not val:
            errs.append(f"{key} must be a non-empty array")
    if isinstance(doc.get("epiphanies"), list):
        for i, ep in enumerate(doc["epiphanies"]):
            if not isinstance(ep, dict) or not str(ep.get("insight", "")).strip():
                errs.append(f"epiphanies[{i}] needs non-empty insight")
    return errs

