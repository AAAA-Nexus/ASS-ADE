# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tdmi.py:7
# Component id: at.source.a1_at_functions.tdmi
from __future__ import annotations

__version__ = "0.1.0"

def tdmi(self):
    if self._tdmi is None:
        from ass_ade.agent.tdmi import TDMI
        self._tdmi = TDMI(self._config, self._nexus)
    return self._tdmi
