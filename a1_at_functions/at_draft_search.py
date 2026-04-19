# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_search.py:7
# Component id: at.source.a1_at_functions.search
from __future__ import annotations

__version__ = "0.1.0"

def search(self) -> list[Arch]:
    self._searches += 1
    base = [
        Arch(name="linear", score=0.5, traits=["simple"]),
        Arch(name="tree", score=0.7, traits=["recursive"]),
        Arch(name="graph", score=0.8, traits=["emergent"]),
    ]
    return sorted(base, key=lambda a: a.score, reverse=True)
