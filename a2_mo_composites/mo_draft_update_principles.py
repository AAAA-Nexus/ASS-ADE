# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_wisdomengine.py:148
# Component id: mo.source.a2_mo_composites.update_principles
from __future__ import annotations

__version__ = "0.1.0"

def update_principles(self, principles: list[str]) -> list[str]:
    for p in principles:
        if p not in self._principles:
            self._principles.append(p)
