"""Tier a2 — assimilated method 'AnthropicProvider.__init__'

Assimilated from: provider.py:181-197
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
def __init__(
    self,
    *,
    api_key: str,
    model: str = "claude-sonnet-4-20250514",
    timeout: float = 120.0,
) -> None:
    self._client = httpx.Client(
        base_url="https://api.anthropic.com",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        timeout=timeout,
    )
    self._default_model = model

