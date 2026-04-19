# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_exif_explore.py:7
# Component id: at.source.a1_at_functions.exif_explore
from __future__ import annotations

__version__ = "0.1.0"

def exif_explore(self, missing_skill: str, env: dict | None = None):
    return self._get_exif().explore(missing_skill, env or {"name": "default"})
