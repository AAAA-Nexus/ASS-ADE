# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:176
# Component id: qk.source.ass_ade.test_estimate_conversation
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
