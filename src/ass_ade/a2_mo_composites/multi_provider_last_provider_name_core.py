"""Tier a2 — assimilated method 'MultiProvider.last_provider_name'

Assimilated from: provider.py:316-317
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
def last_provider_name(self) -> str | None:
    return self._last_provider_name

