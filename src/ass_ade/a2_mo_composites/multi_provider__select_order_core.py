"""Tier a2 — assimilated method 'MultiProvider._select_order'

Assimilated from: provider.py:368-377
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
def _select_order(self, model: str | None) -> list[str]:
    """Compute provider-try order for a given model."""
    if not model:
        return list(self._fallback_order)
    primary = self._model_to_provider.get(model)
    if primary is None:
        return list(self._fallback_order)
    order = [primary]
    order.extend(n for n in self._fallback_order if n != primary)
    return order

