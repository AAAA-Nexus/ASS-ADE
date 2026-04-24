"""Tests for engine.tokens — token estimation and budget management."""

from __future__ import annotations

from ass_ade.engine.tokens import (
    DEFAULT_CONTEXT_WINDOW,
    RESPONSE_RESERVE,
    TokenBudget,
    context_window_for,
    estimate_message_tokens,
    estimate_tokens,
    estimate_tools_tokens,
)
from ass_ade.engine.types import Message, ToolSchema

# ── estimate_tokens ───────────────────────────────────────────────────────────


class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 1  # min 1

    def test_short_text(self):
        result = estimate_tokens("hello world")
        assert result >= 1
        assert result <= 10

    def test_code_block(self):
        code = "def fibonacci(n: int) -> int:\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n"
        result = estimate_tokens(code)
        assert result >= 10
        assert result <= 100

    def test_long_text(self):
        text = "The quick brown fox jumps over the lazy dog. " * 100
        result = estimate_tokens(text)
        # ~4500 chars / 3.7 ≈ ~1216 tokens
        assert 800 < result < 2000

    def test_returns_int(self):
        assert isinstance(estimate_tokens("test"), int)


# ── estimate_message_tokens ───────────────────────────────────────────────────


class TestEstimateMessageTokens:
    def test_simple_user_message(self):
        msg = Message(role="user", content="Hello!")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5  # 4 overhead + at least 1 content

    def test_empty_content(self):
        msg = Message(role="assistant", content="")
        tokens = estimate_message_tokens(msg)
        assert tokens == 4  # just overhead

    def test_message_with_name(self):
        msg = Message(role="tool", content="result", name="read_file")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 6  # overhead + name + content

    def test_system_message(self):
        msg = Message(role="system", content="You are an AI assistant.")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5


# ── estimate_tools_tokens ─────────────────────────────────────────────────────


class TestEstimateToolsTokens:
    def test_empty_list(self):
        assert estimate_tools_tokens([]) == 0

    def test_single_tool(self):
        tool = ToolSchema(
            name="read_file",
            description="Read a file",
            parameters={"type": "object", "properties": {"path": {"type": "string"}}},
        )
        tokens = estimate_tools_tokens([tool])
        assert tokens > 0

    def test_multiple_tools(self):
        tools = [
            ToolSchema(name=f"tool_{i}", description=f"Tool number {i}", parameters={"type": "object"})
            for i in range(5)
        ]
        tokens = estimate_tools_tokens(tools)
        assert tokens > estimate_tools_tokens(tools[:1])


# ── context_window_for ────────────────────────────────────────────────────────


class TestContextWindowFor:
    def test_known_model(self):
        assert context_window_for("gpt-4o") == 128_000

    def test_claude_model(self):
        assert context_window_for("claude-opus-4") == 200_000

    def test_unknown_model(self):
        assert context_window_for("totally-unknown-model") == DEFAULT_CONTEXT_WINDOW

    def test_none_model(self):
        assert context_window_for(None) == DEFAULT_CONTEXT_WINDOW

    def test_fuzzy_match(self):
        # Should match "llama-3.1-8b" as substring
        assert context_window_for("ollama/llama-3.1-8b") == 128_000

    def test_case_insensitive(self):
        assert context_window_for("GPT-4O") == 128_000


# ── TokenBudget ───────────────────────────────────────────────────────────────


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
