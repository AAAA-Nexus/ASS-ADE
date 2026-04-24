"""Tier a2 — assimilated method 'MultiProvider.providers'

Assimilated from: provider.py:312-313
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
def providers(self) -> dict[str, "ModelProvider"]:
    return dict(self._providers)

