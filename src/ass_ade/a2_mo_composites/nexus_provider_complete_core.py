"""Tier a2 — assimilated method 'NexusProvider.complete'

Assimilated from: provider.py:395-412
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
def complete(self, request: CompletionRequest) -> CompletionResponse:
    prompt = self._messages_to_prompt(request.messages, request.tools)
    result = self._client.inference(prompt)

    text = result.result or result.text or ""

    # Parse tool calls from the response if tools were provided
    tool_calls, content = self._parse_tool_calls(text, request.tools)

    return CompletionResponse(
        message=Message(
            role="assistant",
            content=content,
            tool_calls=tool_calls,
        ),
        model=result.model or "nexus-inference",
        finish_reason="tool_calls" if tool_calls else "stop",
    )

