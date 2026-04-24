"""Tier a2 — assimilated method 'MultiProvider.complete'

Assimilated from: provider.py:345-366
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
    """Route a request to the right provider, with automatic fallback."""
    order = self._select_order(request.model)
    last_error: Exception | None = None
    for name in order:
        provider = self._providers.get(name)
        if provider is None:
            continue
        try:
            response = provider.complete(request)
            self._last_provider_name = name
            return response
        except httpx.HTTPError as exc:
            last_error = exc
            continue
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
    # All providers failed — re-raise the last error so the caller sees it.
    if last_error is not None:
        raise last_error
    raise RuntimeError("MultiProvider: no providers configured")

