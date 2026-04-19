# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_epistemicrouter.py:43
# Component id: sy.source.a4_sy_orchestration.history
from __future__ import annotations

__version__ = "0.1.0"

def history(self) -> list[RoutingDecision]:
    return list(self._history)
