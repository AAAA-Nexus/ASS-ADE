# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:69
# Component id: mo.source.a2_mo_composites.wisdom
from __future__ import annotations

__version__ = "0.1.0"

def wisdom(self):
    if self._wisdom is None:
        from ass_ade.agent.wisdom import WisdomEngine
        self._wisdom = WisdomEngine(self._config, self._nexus)
        # Hydrate principles + conviction from prior sessions (Phase 4)
        self._hydrate_wisdom(self._wisdom)
    return self._wisdom
