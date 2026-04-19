# Extracted from C:/!ass-ade/src/ass_ade/agent/edee.py:85
# Component id: at.source.ass_ade.exif_explore
from __future__ import annotations

__version__ = "0.1.0"

def exif_explore(self, missing_skill: str, env: dict | None = None):
    return self._get_exif().explore(missing_skill, env or {"name": "default"})
