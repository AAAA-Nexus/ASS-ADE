# Extracted from C:/!ass-ade/src/ass_ade/agent/severa.py:28
# Component id: at.source.ass_ade.search
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
