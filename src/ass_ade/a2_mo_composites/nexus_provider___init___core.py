"""Tier a2 — assimilated method 'NexusProvider.__init__'

Assimilated from: provider.py:388-389
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
def __init__(self, client: Any) -> None:
    self._client = client

