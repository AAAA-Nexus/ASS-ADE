# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:248
# Component id: sy.source.ass_ade.ide
from __future__ import annotations

__version__ = "0.1.0"

def ide(self):
    if self._ide is None:
        from ass_ade.agent.ide import IDE
        self._ide = IDE(self._config, self._nexus)
    return self._ide
