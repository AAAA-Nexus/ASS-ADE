"""Tier a2 — assimilated method 'MultiProvider.register'

Assimilated from: provider.py:328-334
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
def register(self, name: str, provider: "ModelProvider", models: list[str] | None = None) -> None:
    """Add a provider to the router at runtime."""
    self._providers[name] = provider
    if name not in self._fallback_order:
        self._fallback_order.append(name)
    for m in models or []:
        self._model_to_provider[m] = name

