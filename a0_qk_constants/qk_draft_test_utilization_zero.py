# Extracted from C:/!ass-ade/tests/test_tokens.py:131
# Component id: qk.source.ass_ade.test_utilization_zero
from __future__ import annotations

__version__ = "0.1.0"

def test_utilization_zero(self):
    budget = TokenBudget(context_window=10_000)
    assert budget.utilization == 0.0
