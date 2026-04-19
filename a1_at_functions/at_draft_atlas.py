# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_atlas.py:7
# Component id: at.source.a1_at_functions.atlas
from __future__ import annotations

__version__ = "0.1.0"

def atlas(self):
    if self._atlas is None:
        from ass_ade.agent.atlas import Atlas
        self._atlas = Atlas(self._config, self._nexus)
    return self._atlas
