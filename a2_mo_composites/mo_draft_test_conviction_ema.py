# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwisdomengine.py:44
# Component id: mo.source.a2_mo_composites.test_conviction_ema
from __future__ import annotations

__version__ = "0.1.0"

def test_conviction_ema(self) -> None:
    w = WisdomEngine({})
    r1 = w.run_audit({})  # score 0, conviction = 0.5*0.5 + 0.5*0 = 0.25
    assert abs(w.conviction - 0.25) < 0.01
    assert not w.is_confident  # well below 0.85
