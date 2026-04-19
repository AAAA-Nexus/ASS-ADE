# Extracted from C:/!ass-ade/tests/test_phase_engines.py:40
# Component id: mo.source.ass_ade.test_high_trs_simple_task_gives_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_high_trs_simple_task_gives_fast(self):
    lse = self._make()
    decision = lse.select(trs_score=0.95, complexity="simple")
    assert decision.tier == "fast"
