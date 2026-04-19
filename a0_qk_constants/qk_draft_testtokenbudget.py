# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:121
# Component id: qk.source.ass_ade.testtokenbudget
__version__ = "0.1.0"

class TestTokenBudget:
    def test_for_model(self):
        budget = TokenBudget.for_model("gpt-4o")
        assert budget.context_window == 128_000
        assert budget.reserve == RESPONSE_RESERVE

    def test_available(self):
        budget = TokenBudget(context_window=10_000, reserve=1000)
        assert budget.available == 9000

    def test_utilization_zero(self):
        budget = TokenBudget(context_window=10_000)
        assert budget.utilization == 0.0

    def test_utilization_after_update(self):
        budget = TokenBudget(context_window=10_000)
        budget.update_from_usage({"prompt_tokens": 5000, "completion_tokens": 100})
        assert budget.utilization == 0.5
        assert budget.completion_tokens == 100
        assert budget.total_calls == 1

    def test_update_none_usage(self):
        budget = TokenBudget(context_window=10_000)
        budget.update_from_usage(None)
        assert budget.total_calls == 0

    def test_messages_to_evict_within_budget(self):
        budget = TokenBudget(context_window=100_000)
        messages = [
            Message(role="system", content="System prompt"),
            Message(role="user", content="Hello"),
        ]
        assert budget.messages_to_evict(messages) == 0

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

    def test_system_messages_not_evicted(self):
        budget = TokenBudget(context_window=50, reserve=10)
        messages = [
            Message(role="system", content="Important system prompt"),
            Message(role="user", content="A" * 200),
        ]
        evictions = budget.messages_to_evict(messages)
        # Even if over budget, we'd only evict the user message, not system
        assert evictions <= 1

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
