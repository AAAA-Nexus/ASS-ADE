# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:17
# Component id: qk.source.a0_qk_constants.test_utilization_zero
from __future__ import annotations

__version__ = "0.1.0"

def test_utilization_zero(self):
    budget = TokenBudget(context_window=10_000)
    assert budget.utilization == 0.0
