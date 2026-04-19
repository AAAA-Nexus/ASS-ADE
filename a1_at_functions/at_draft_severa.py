# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_severa.py:7
# Component id: at.source.a1_at_functions.severa
from __future__ import annotations

__version__ = "0.1.0"

def severa(self):
    if self._severa is None:
        from ass_ade.agent.severa import Severa
        self._severa = Severa(self._config, self._nexus)
    return self._severa
