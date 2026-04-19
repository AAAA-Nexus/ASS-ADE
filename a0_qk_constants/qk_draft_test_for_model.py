# Extracted from C:/!ass-ade/tests/test_tokens.py:122
# Component id: qk.source.ass_ade.test_for_model
from __future__ import annotations

__version__ = "0.1.0"

def test_for_model(self):
    budget = TokenBudget.for_model("gpt-4o")
    assert budget.context_window == 128_000
    assert budget.reserve == RESPONSE_RESERVE
