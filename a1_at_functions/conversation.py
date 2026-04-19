"""Conversation manager — tracks message history with context-window awareness.

Supports two trimming strategies:
  1. Count-based: trim to a max number of messages (legacy).
  2. Token-aware: trim to fit within a model's context window budget.

The token-aware strategy uses the TokenBudget from engine.tokens to
compute the minimum evictions needed, preserving the system prompt and
the most recent messages.
"""

from __future__ import annotations

from ass_ade.engine.tokens import TokenBudget, estimate_message_tokens
from ass_ade.engine.types import Message, ToolSchema


class Conversation:
    """Manages a conversation's message history with token-aware trimming."""

    def __init__(self, system_prompt: str = "", model: str | None = None) -> None:
        self._messages: list[Message] = []
        self._budget = TokenBudget.for_model(model)
        if system_prompt:
            self._messages.append(Message(role="system", content=system_prompt))

    @property
    def messages(self) -> list[Message]:
        return list(self._messages)

    @property
    def budget(self) -> TokenBudget:
        return self._budget

    def add(self, message: Message) -> None:
        self._messages.append(message)

    def add_user(self, content: str) -> None:
        self._messages.append(Message(role="user", content=content))

    def add_assistant(self, message: Message) -> None:
        self._messages.append(message)

    def add_tool_result(self, tool_call_id: str, name: str, content: str) -> None:
        self._messages.append(
            Message(
                role="tool",
                content=content,
                tool_call_id=tool_call_id,
                name=name,
            )
        )

    def count(self) -> int:
        return len(self._messages)

    def estimated_tokens(self) -> int:
        """Total estimated tokens across all messages."""
        return sum(estimate_message_tokens(m) for m in self._messages)

    def trim(self, max_messages: int = 50) -> int:
        """Trim oldest non-system messages if over limit. Returns count removed."""
        if len(self._messages) <= max_messages:
            return 0

        system = [m for m in self._messages if m.role == "system"]
        others = [m for m in self._messages if m.role != "system"]

        keep = max_messages - len(system)
        removed = len(others) - keep
        if removed <= 0:
            return 0

        self._messages = system + others[removed:]
        return removed

    def trim_to_budget(self, tools: list[ToolSchema] | None = None) -> int:
        """Trim oldest non-system messages to fit within the token budget.

        Uses the TokenBudget invariant:
            Σ tokens(messages) + tokens(tools) + reserve ≤ context_window

        Returns the number of messages evicted.
        """
        to_evict = self._budget.messages_to_evict(self._messages, tools)
        if to_evict == 0:
            return 0

        system = [m for m in self._messages if m.role == "system"]
        others = [m for m in self._messages if m.role != "system"]

        self._messages = system + others[to_evict:]
        return to_evict
