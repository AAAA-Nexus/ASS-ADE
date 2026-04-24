"""Tier a1 — assimilated function 'detect_cycles'

Assimilated from: rebuild/cycle_detector.py:60-94
"""

from __future__ import annotations


# --- assimilated symbol ---
def detect_cycles(plan: dict[str, Any]) -> dict[str, Any]:
    """Detect cycles in the ``made_of`` dependency graph of a rebuild plan.

    Returns a dict with ``cycles``, ``cycle_count``, ``nodes_in_cycles``, ``acyclic``.
    """
    components: list[dict[str, Any]] = plan.get("proposed_components", [])

    graph: dict[str, list[str]] = {}
    for comp in components:
        comp_id: str = comp.get("id", "")
        if not comp_id:
            continue
        deps: list[str] = comp.get("made_of", []) or []
        graph[comp_id] = [d for d in deps if d != comp_id]

    self_loops: list[list[str]] = []
    for comp in components:
        comp_id = comp.get("id", "")
        raw_deps = comp.get("made_of", []) or []
        if comp_id and comp_id in raw_deps:
            self_loops.append([comp_id])

    scc_cycles = _tarjan_scc(graph)
    all_cycles = self_loops + scc_cycles

    nodes_in_cycles: set[str] = set()
    for cycle in all_cycles:
        nodes_in_cycles.update(cycle)

    return {
        "cycles": all_cycles,
        "cycle_count": len(all_cycles),
        "nodes_in_cycles": len(nodes_in_cycles),
        "acyclic": len(all_cycles) == 0,
    }

