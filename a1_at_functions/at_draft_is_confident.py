# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_is_confident.py:7
# Component id: at.source.a1_at_functions.is_confident
from __future__ import annotations

__version__ = "0.1.0"

def is_confident(self) -> bool:
    return self._conviction >= self._conviction_required
