# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcpserver.py:57
# Component id: sy.source.a4_sy_orchestration.cie
from __future__ import annotations

__version__ = "0.1.0"

def cie(self) -> Any:
    if self._cie is None:
        from ass_ade.agent.cie import CIEPipeline
        self._cie = CIEPipeline()
    return self._cie
