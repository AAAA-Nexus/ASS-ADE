# Extracted from C:/!ass-ade/tests/test_tokens.py:127
# Component id: qk.source.ass_ade.test_available
from __future__ import annotations

__version__ = "0.1.0"

def test_available(self):
    budget = TokenBudget(context_window=10_000, reserve=1000)
    assert budget.available == 9000
