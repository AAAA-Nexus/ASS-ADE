# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:209
# Component id: sy.source.ass_ade.tdmi
from __future__ import annotations

__version__ = "0.1.0"

def tdmi(self):
    if self._tdmi is None:
        from ass_ade.agent.tdmi import TDMI
        self._tdmi = TDMI(self._config, self._nexus)
    return self._tdmi
