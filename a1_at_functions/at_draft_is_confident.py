# Extracted from C:/!ass-ade/src/ass_ade/agent/wisdom.py:56
# Component id: at.source.ass_ade.is_confident
from __future__ import annotations

__version__ = "0.1.0"

def is_confident(self) -> bool:
    return self._conviction >= self._conviction_required
