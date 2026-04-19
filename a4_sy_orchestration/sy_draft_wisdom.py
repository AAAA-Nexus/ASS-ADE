# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:143
# Component id: sy.source.ass_ade.wisdom
from __future__ import annotations

__version__ = "0.1.0"

def wisdom(self):
    if self._wisdom is None:
        from ass_ade.agent.wisdom import WisdomEngine
        self._wisdom = WisdomEngine(self._config, self._nexus)
        # Hydrate principles + conviction from prior sessions (Phase 4)
        self._hydrate_wisdom(self._wisdom)
    return self._wisdom
