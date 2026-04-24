"""Tier a2 — assimilated method 'NexusProvider._parse_tool_calls'

Assimilated from: provider.py:438-459
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
def _parse_tool_calls(
    text: str, tools: list[Any]
) -> tuple[list[ToolCallRequest], str]:
    if not tools:
        return [], text

    # Try to extract a JSON tool call from the response
    try:
        data = json.loads(text.strip())
        if isinstance(data, dict) and "tool_call" in data:
            tc = data["tool_call"]
            return [
                ToolCallRequest(
                    id=f"call_{uuid.uuid4().hex[:8]}",
                    name=tc["name"],
                    arguments=tc.get("arguments", {}),
                )
            ], ""
    except (json.JSONDecodeError, KeyError, TypeError):
        pass

    return [], text

