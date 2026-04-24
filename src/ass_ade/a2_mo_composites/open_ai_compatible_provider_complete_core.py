"""Tier a2 — assimilated method 'OpenAICompatibleProvider.complete'

Assimilated from: provider.py:65-124
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
    model = request.model or self._default_model
    body: dict[str, Any] = {
        "model": model,
        "messages": [self._format_message(m) for m in request.messages],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
    }
    if request.tools:
        body["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in request.tools
        ]

    resp = self._client.post(self._completions_path, json=body)
    resp.raise_for_status()
    data = resp.json()

    choice = data["choices"][0]
    msg_data = choice["message"]

    tool_calls: list[ToolCallRequest] = []
    if raw_calls := msg_data.get("tool_calls"):
        for tc in raw_calls:
            fn = tc["function"]
            try:
                args = (
                    json.loads(fn["arguments"])
                    if isinstance(fn["arguments"], str)
                    else fn["arguments"]
                )
            except json.JSONDecodeError:
                args = {"raw": fn["arguments"]}
            tool_calls.append(
                ToolCallRequest(
                    id=tc["id"],
                    name=fn["name"],
                    arguments=args,
                )
            )

    message = Message(
        role="assistant",
        content=msg_data.get("content") or "",
        tool_calls=tool_calls,
    )

    return CompletionResponse(
        message=message,
        model=data.get("model"),
        finish_reason=choice.get("finish_reason"),
        usage=data.get("usage"),
    )

