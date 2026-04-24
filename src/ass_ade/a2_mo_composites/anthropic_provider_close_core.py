"""Tier a2 — assimilated method 'AnthropicProvider.close'

Assimilated from: provider.py:199-200
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
    self._client.close()

