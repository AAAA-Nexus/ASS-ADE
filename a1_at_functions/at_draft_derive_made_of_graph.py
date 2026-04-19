# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_derive_made_of_graph.py:7
# Component id: at.source.a1_at_functions.derive_made_of_graph
from __future__ import annotations

__version__ = "0.1.0"

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
