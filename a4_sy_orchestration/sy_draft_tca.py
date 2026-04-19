# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcpserver.py:50
# Component id: sy.source.a4_sy_orchestration.tca
from __future__ import annotations

__version__ = "0.1.0"

def tca(self) -> Any:
    if self._tca is None:
        from ass_ade.agent.tca import TCAEngine
        self._tca = TCAEngine({"working_dir": self._working_dir})
    return self._tca
