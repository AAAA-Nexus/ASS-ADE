# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_budget_pressure_downgrades_to_fast.py:7
# Component id: at.source.a1_at_functions.test_budget_pressure_downgrades_to_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_budget_pressure_downgrades_to_fast(self):
    lse = self._make()
    decision = lse.select(trs_score=0.8, complexity="complex", budget_remaining=500)
    assert decision.tier == "fast"
    assert "budget_pressure" in decision.reason
