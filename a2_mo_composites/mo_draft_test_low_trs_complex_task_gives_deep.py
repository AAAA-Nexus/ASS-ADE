# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseengine.py:35
# Component id: mo.source.a2_mo_composites.test_low_trs_complex_task_gives_deep
from __future__ import annotations

__version__ = "0.1.0"

def test_low_trs_complex_task_gives_deep(self):
    lse = self._make()
    decision = lse.select(trs_score=0.3, complexity="complex")
    assert decision.tier == "deep"
