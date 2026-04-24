"""Tier a1 — assimilated function 'derive_made_of_graph'

Assimilated from: rebuild/body_extractor.py:175-190
"""

from __future__ import annotations


# --- assimilated symbol ---
def derive_made_of_graph(plan: dict[str, Any]) -> dict[str, Any]:
    """Populate each component's ``made_of`` from call-graph analysis. Mutates ``plan``."""
    by_name: dict[str, str] = {}
    for prop in plan.get("proposed_components") or []:
        name = (prop.get("name") or "").lower()
        if name:
            by_name[name] = prop["id"]

    for prop in plan.get("proposed_components") or []:
        made_of: list[str] = list(prop.get("made_of") or [])
        for callee in prop.get("callers_of") or []:
            target_id = by_name.get((callee or "").lower())
            if target_id and target_id != prop["id"] and target_id not in made_of:
                made_of.append(target_id)
        prop["made_of"] = made_of
    return plan

