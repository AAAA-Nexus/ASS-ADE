# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:13
# Component id: qk.source.a0_qk_constants.test_available
from __future__ import annotations

__version__ = "0.1.0"

def test_available(self):
    budget = TokenBudget(context_window=10_000, reserve=1000)
    assert budget.available == 9000
