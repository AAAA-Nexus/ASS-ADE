# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseengine.py:30
# Component id: mo.source.a2_mo_composites.test_high_trs_simple_task_gives_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_high_trs_simple_task_gives_fast(self):
    lse = self._make()
    decision = lse.select(trs_score=0.95, complexity="simple")
    assert decision.tier == "fast"
