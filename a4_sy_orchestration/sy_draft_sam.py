# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:241
# Component id: sy.source.ass_ade.sam
from __future__ import annotations

__version__ = "0.1.0"

def sam(self):
    if self._sam is None:
        from ass_ade.agent.sam import SAM
        self._sam = SAM(self._config, self._nexus)
    return self._sam
