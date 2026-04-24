"""Tier a2 — assimilated class 'TokenBudget'

Assimilated from: tokens.py:166-256
"""

from __future__ import annotations


# --- assimilated symbol ---
class TokenBudget:
    """Tracks token usage against a model's context window.

    Invariant maintained:
        used + tool_overhead + reserve ≤ context_window

    When the invariant would be violated, ``messages_to_evict()``
    returns the number of oldest non-system messages to drop.
    """

    context_window: int
    reserve: int = RESPONSE_RESERVE

    # Running totals
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_calls: int = 0

    @classmethod
    def for_model(cls, model: str | None) -> TokenBudget:
        return cls(context_window=context_window_for(model))

    @property
    def available(self) -> int:
        """Tokens available for prompt content (messages + tools)."""
        return max(0, self.context_window - self.reserve)

    @property
    def utilization(self) -> float:
        """Fraction of context window currently used (0.0 – 1.0)."""
        if self.context_window == 0:
            return 1.0
        return min(1.0, self.prompt_tokens / self.context_window)

    def update_from_usage(self, usage: dict[str, int] | None) -> None:
        """Update running totals from a completion response's usage dict."""
        if not usage:
            return
        self.prompt_tokens = usage.get("prompt_tokens", self.prompt_tokens)
        self.completion_tokens += usage.get("completion_tokens", 0)
        self.total_calls += 1

    def messages_to_evict(
        self,
        messages: list[Message],
        tools: list[ToolSchema] | None = None,
    ) -> int:
        """Compute how many oldest non-system messages to evict.

        Returns 0 if the conversation fits within the budget.
        The eviction count is the *minimum* needed to restore the invariant.
        """
        tool_overhead = estimate_tools_tokens(tools or [])

        # Calculate cumulative tokens for each message
        msg_tokens = [estimate_message_tokens(m) for m in messages]
        total = sum(msg_tokens) + tool_overhead

        if total <= self.available:
            return 0

        # Identify non-system messages eligible for eviction
        excess = total - self.available
        evicted = 0
        freed = 0
        for i, msg in enumerate(messages):
            if msg.role == "system":
                continue
            freed += msg_tokens[i]
            evicted += 1
            if freed >= excess:
                break

        return evicted

    def estimate_conversation(
        self,
        messages: list[Message],
        tools: list[ToolSchema] | None = None,
    ) -> dict[str, int]:
        """Return a breakdown of token usage for the current conversation."""
        msg_tokens = sum(estimate_message_tokens(m) for m in messages)
        tool_tokens = estimate_tools_tokens(tools or [])
        return {
            "message_tokens": msg_tokens,
            "tool_schema_tokens": tool_tokens,
            "reserve": self.reserve,
            "total_needed": msg_tokens + tool_tokens + self.reserve,
            "context_window": self.context_window,
            "headroom": max(0, self.context_window - msg_tokens - tool_tokens - self.reserve),
        }

