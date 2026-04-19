# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:21
# Component id: qk.source.a0_qk_constants.test_utilization_after_update
from __future__ import annotations

__version__ = "0.1.0"

def test_utilization_after_update(self):
    budget = TokenBudget(context_window=10_000)
    budget.update_from_usage({"prompt_tokens": 5000, "completion_tokens": 100})
    assert budget.utilization == 0.5
    assert budget.completion_tokens == 100
    assert budget.total_calls == 1
