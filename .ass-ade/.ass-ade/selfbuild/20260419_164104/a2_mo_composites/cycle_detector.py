"""Cycle Detector — detect and break dependency cycles in a rebuild plan.

Uses Tarjan's SCC algorithm over the ``made_of`` graph.
"""

from __future__ import annotations

from typing import Any


def _tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """Return all strongly-connected components with more than one node.

    Iterative Tarjan's algorithm — avoids Python recursion limits on large graphs.
    """
    index_counter = [0]
    stack: list[str] = []
    lowlinks: dict[str, int] = {}
    index: dict[str, int] = {}
    on_stack: dict[str, bool] = {}
    sccs: list[list[str]] = []

    all_nodes: set[str] = set(graph.keys())
    for deps in graph.values():
        all_nodes.update(deps)
    full_graph: dict[str, list[str]] = {n: graph.get(n, []) for n in all_nodes}

    def strongconnect(v: str) -> None:
        index[v] = index_counter[0]
        lowlinks[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in full_graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif on_stack.get(w, False):
                lowlinks[v] = min(lowlinks[v], index[w])

        if lowlinks[v] == index[v]:
            scc: list[str] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1:
                sccs.append(scc)

    for node in sorted(full_graph):
        if node not in index:
            strongconnect(node)

    return sccs


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


def validate_acyclic(plan: dict[str, Any]) -> bool:
    """Return True iff the plan's ``made_of`` graph contains no cycles."""
    return detect_cycles(plan)["acyclic"]
