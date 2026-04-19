# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lse.py:7
# Component id: at.source.a1_at_functions.lse
from __future__ import annotations

__version__ = "0.1.0"

def lse(self):
    if self._lse is None:
        from ass_ade.agent.lse import LSEEngine
        self._lse = LSEEngine(self._config, self._nexus)
    return self._lse
