# Extracted from C:/!ass-ade/tests/test_phase_engines.py:50
# Component id: mo.source.ass_ade.test_critical_complexity_always_deep
from __future__ import annotations

__version__ = "0.1.0"

def test_critical_complexity_always_deep(self):
    lse = self._make()
    decision = lse.select(trs_score=0.9, complexity="critical")
    assert decision.tier == "deep"
