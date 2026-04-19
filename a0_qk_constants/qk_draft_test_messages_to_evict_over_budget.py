# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:41
# Component id: qk.source.a0_qk_constants.test_messages_to_evict_over_budget
from __future__ import annotations

__version__ = "0.1.0"

def test_messages_to_evict_over_budget(self):
    budget = TokenBudget(context_window=50, reserve=10)  # very small
    messages = [
        Message(role="system", content="System prompt"),
        Message(role="user", content="A" * 200),
        Message(role="assistant", content="B" * 200),
        Message(role="user", content="C" * 50),
    ]
    evictions = budget.messages_to_evict(messages)
    assert evictions > 0
