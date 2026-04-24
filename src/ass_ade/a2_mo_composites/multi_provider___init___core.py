"""Tier a2 — assimilated method 'MultiProvider.__init__'

Assimilated from: provider.py:300-309
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
    providers: dict[str, "ModelProvider"],
    model_to_provider: dict[str, str] | None = None,
    fallback_order: list[str] | None = None,
) -> None:
    self._providers = dict(providers)
    self._model_to_provider = dict(model_to_provider or {})
    self._fallback_order = list(fallback_order or providers.keys())
    self._last_provider_name: str | None = None

