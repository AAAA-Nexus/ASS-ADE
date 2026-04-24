"""Tier a2 — assimilated method 'MultiProvider.close'

Assimilated from: provider.py:336-343
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
def close(self) -> None:
    for p in self._providers.values():
        close = getattr(p, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass

