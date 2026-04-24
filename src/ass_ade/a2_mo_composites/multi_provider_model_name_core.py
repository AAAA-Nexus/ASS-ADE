"""Tier a2 — assimilated method 'MultiProvider.model_name'

Assimilated from: provider.py:320-326
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
def model_name(self) -> str:
    # For compatibility with the OpenAICompatibleProvider property
    if self._providers and self._fallback_order:
        first = self._providers.get(self._fallback_order[0])
        if first is not None and hasattr(first, "model_name"):
            return first.model_name  # type: ignore[no-any-return]
    return "multi-provider"

