# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_for_model.py:7
# Component id: qk.source.a0_qk_constants.test_for_model
from __future__ import annotations

__version__ = "0.1.0"

def test_for_model(self):
    budget = TokenBudget.for_model("gpt-4o")
    assert budget.context_window == 128_000
    assert budget.reserve == RESPONSE_RESERVE
