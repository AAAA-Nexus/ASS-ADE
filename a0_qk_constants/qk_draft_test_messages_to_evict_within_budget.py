# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:33
# Component id: qk.source.a0_qk_constants.test_messages_to_evict_within_budget
from __future__ import annotations

__version__ = "0.1.0"

def test_messages_to_evict_within_budget(self):
    budget = TokenBudget(context_window=100_000)
    messages = [
        Message(role="system", content="System prompt"),
        Message(role="user", content="Hello"),
    ]
    assert budget.messages_to_evict(messages) == 0
