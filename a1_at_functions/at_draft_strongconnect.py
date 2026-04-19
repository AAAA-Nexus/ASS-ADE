# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_strongconnect.py:7
# Component id: at.source.a1_at_functions.strongconnect
from __future__ import annotations

__version__ = "0.1.0"

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
