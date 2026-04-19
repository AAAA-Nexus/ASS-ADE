# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ide.py:7
# Component id: at.source.a1_at_functions.ide
from __future__ import annotations

__version__ = "0.1.0"

def ide(self):
    if self._ide is None:
        from ass_ade.agent.ide import IDE
        self._ide = IDE(self._config, self._nexus)
    return self._ide
