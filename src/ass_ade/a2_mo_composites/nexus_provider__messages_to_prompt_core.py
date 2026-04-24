"""Tier a2 — assimilated method 'NexusProvider._messages_to_prompt'

Assimilated from: provider.py:415-435
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
import uuid
from collections.abc import Iterator
from typing import Any, Protocol, runtime_checkable

import httpx

from ass_ade.engine.types import (


# --- assimilated symbol ---
def _messages_to_prompt(messages: list[Message], tools: list[Any]) -> str:
    parts: list[str] = []
    for msg in messages:
        if msg.role == "system":
            parts.append(f"[System]\n{msg.content}")
        elif msg.role == "user":
            parts.append(f"[User]\n{msg.content}")
        elif msg.role == "assistant":
            parts.append(f"[Assistant]\n{msg.content}")
        elif msg.role == "tool":
            parts.append(f"[Tool Result: {msg.name}]\n{msg.content}")

    if tools:
        tool_desc = "\n".join(f"- {t.name}: {t.description}" for t in tools)
        parts.append(f"\nAvailable tools:\n{tool_desc}")
        parts.append(
            '\nTo call a tool, respond with exactly this JSON format: '
            '{"tool_call": {"name": "tool_name", "arguments": {...}}}'
        )

    return "\n\n".join(parts)

