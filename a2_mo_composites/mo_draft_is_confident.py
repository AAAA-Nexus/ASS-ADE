# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_wisdomengine.py:25
# Component id: mo.source.a2_mo_composites.is_confident
from __future__ import annotations

__version__ = "0.1.0"

def is_confident(self) -> bool:
    return self._conviction >= self._conviction_required
