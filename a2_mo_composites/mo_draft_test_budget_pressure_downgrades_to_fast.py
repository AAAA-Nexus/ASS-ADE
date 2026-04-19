# Extracted from C:/!ass-ade/tests/test_phase_engines.py:61
# Component id: mo.source.ass_ade.test_budget_pressure_downgrades_to_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_budget_pressure_downgrades_to_fast(self):
    lse = self._make()
    decision = lse.select(trs_score=0.8, complexity="complex", budget_remaining=500)
    assert decision.tier == "fast"
    assert "budget_pressure" in decision.reason
