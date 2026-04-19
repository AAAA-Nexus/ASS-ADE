# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/cycle_detector.py:97
# Component id: mo.source.ass_ade.break_cycles
from __future__ import annotations

__version__ = "0.1.0"

def break_cycles(plan: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Remove the minimum set of edges required to break all detected cycles.

    Strategy: for each cycle the lexicographically-last node is the breaker —
    its id is removed from the ``made_of`` of every other cycle member.
    Mutates ``plan`` in place.
    """
    cycles: list[list[str]] = report.get("cycles", [])
    if not cycles:
        return {"edges_removed": 0, "nodes_affected": []}

    comp_index: dict[str, dict[str, Any]] = {}
    for comp in plan.get("proposed_components", []):
        comp_id = comp.get("id", "")
        if comp_id:
            comp_index[comp_id] = comp

    edges_removed = 0
    nodes_affected_set: set[str] = set()

    for cycle in cycles:
        if not cycle:
            continue

        if len(cycle) == 1:
            node_id = cycle[0]
            comp = comp_index.get(node_id)
            if comp is not None:
                before = len(comp.get("made_of", []) or [])
                comp["made_of"] = [d for d in (comp.get("made_of") or []) if d != node_id]
                removed = before - len(comp["made_of"])
                if removed:
                    edges_removed += removed
                    nodes_affected_set.add(node_id)
            continue

        breaker = max(cycle)
        for member_id in (n for n in cycle if n != breaker):
            comp = comp_index.get(member_id)
            if comp is None:
                continue
            made_of: list[str] = list(comp.get("made_of") or [])
            new_made_of = [d for d in made_of if d != breaker]
            removed = len(made_of) - len(new_made_of)
            if removed:
                comp["made_of"] = new_made_of
                edges_removed += removed
                nodes_affected_set.add(member_id)

    return {
        "edges_removed": edges_removed,
        "nodes_affected": sorted(nodes_affected_set),
    }
