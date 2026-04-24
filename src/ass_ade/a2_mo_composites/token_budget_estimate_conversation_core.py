"""Tier a2 — assimilated method 'TokenBudget.estimate_conversation'

Assimilated from: tokens.py:241-256
"""

from __future__ import annotations


# --- assimilated symbol ---
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

