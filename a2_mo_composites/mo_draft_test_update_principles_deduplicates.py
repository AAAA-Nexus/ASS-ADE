# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwisdomengine.py:90
# Component id: mo.source.a2_mo_composites.test_update_principles_deduplicates
from __future__ import annotations

__version__ = "0.1.0"

def test_update_principles_deduplicates(self) -> None:
    w = WisdomEngine({})
    w.update_principles(["prefer reuse over regeneration"])
    w.update_principles(["prefer reuse over regeneration", "new principle"])
    assert w._principles.count("prefer reuse over regeneration") == 1
    assert "new principle" in w._principles
