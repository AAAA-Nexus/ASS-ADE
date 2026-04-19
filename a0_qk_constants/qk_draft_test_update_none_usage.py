# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:28
# Component id: qk.source.a0_qk_constants.test_update_none_usage
from __future__ import annotations

__version__ = "0.1.0"

def test_update_none_usage(self):
    budget = TokenBudget(context_window=10_000)
    budget.update_from_usage(None)
    assert budget.total_calls == 0
