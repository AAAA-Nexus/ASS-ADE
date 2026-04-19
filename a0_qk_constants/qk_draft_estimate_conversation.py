# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_estimate_conversation.py:7
# Component id: qk.source.a0_qk_constants.estimate_conversation
from __future__ import annotations

__version__ = "0.1.0"

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
