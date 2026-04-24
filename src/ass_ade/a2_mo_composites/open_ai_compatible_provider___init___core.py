"""Tier a2 — assimilated method 'OpenAICompatibleProvider.__init__'

Assimilated from: provider.py:34-56
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
    base_url: str = "https://api.openai.com/v1",
    api_key: str = "",
    model: str = "gpt-4o",
    timeout: float = 120.0,
    completions_path: str = "/chat/completions",
    auth_scheme: str = "bearer",
) -> None:
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if api_key:
        if auth_scheme == "x-api-key":
            headers["x-api-key"] = api_key
        else:
            headers["Authorization"] = f"Bearer {api_key}"
    self._client = httpx.Client(
        base_url=base_url.rstrip("/"),
        headers=headers,
        timeout=timeout,
    )
    self._default_model = model
    self._completions_path = completions_path

