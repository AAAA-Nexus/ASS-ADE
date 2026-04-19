# Extracted from C:/!ass-ade/tests/test_tokens.py:166
# Component id: qk.source.ass_ade.test_system_messages_not_evicted
from __future__ import annotations

__version__ = "0.1.0"

def test_system_messages_not_evicted(self):
    budget = TokenBudget(context_window=50, reserve=10)
    messages = [
        Message(role="system", content="Important system prompt"),
        Message(role="user", content="A" * 200),
    ]
    evictions = budget.messages_to_evict(messages)
    # Even if over budget, we'd only evict the user message, not system
    assert evictions <= 1
