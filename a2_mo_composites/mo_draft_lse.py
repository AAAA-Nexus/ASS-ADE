# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:188
# Component id: mo.source.a2_mo_composites.lse
from __future__ import annotations

__version__ = "0.1.0"

def lse(self):
    if self._lse is None:
        from ass_ade.agent.lse import LSEEngine
        self._lse = LSEEngine(self._config, self._nexus)
    return self._lse
