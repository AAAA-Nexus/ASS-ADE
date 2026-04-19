# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtokenbudget.py:62
# Component id: qk.source.a0_qk_constants.test_estimate_conversation
from __future__ import annotations

__version__ = "0.1.0"

def test_estimate_conversation(self):
    budget = TokenBudget(context_window=100_000)
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Tell me about Python."),
    ]
    estimate = budget.estimate_conversation(messages)
    assert "message_tokens" in estimate
    assert "tool_schema_tokens" in estimate
    assert "reserve" in estimate
    assert "total_needed" in estimate
    assert "context_window" in estimate
    assert "headroom" in estimate
    assert estimate["context_window"] == 100_000
    assert estimate["headroom"] > 0
