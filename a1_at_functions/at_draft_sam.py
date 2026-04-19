# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_sam.py:7
# Component id: at.source.a1_at_functions.sam
from __future__ import annotations

__version__ = "0.1.0"

def sam(self):
    if self._sam is None:
        from ass_ade.agent.sam import SAM
        self._sam = SAM(self._config, self._nexus)
    return self._sam
