"""Tier a2 — assimilated method 'OpenAICompatibleProvider.stream'

Assimilated from: provider.py:126-150
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
def stream(self, request: CompletionRequest) -> Iterator[str]:
    """Streaming variant — yields text chunks."""
    model = request.model or self._default_model
    body: dict[str, Any] = {
        "model": model,
        "messages": [self._format_message(m) for m in request.messages],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "stream": True,
    }
    with self._client.stream("POST", self._completions_path, json=body) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line or not line.startswith("data: "):
                continue
            payload = line[6:]
            if payload.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(payload)
                delta = chunk["choices"][0].get("delta", {})
                if text := delta.get("content"):
                    yield text
            except (json.JSONDecodeError, KeyError, IndexError):
                continue

