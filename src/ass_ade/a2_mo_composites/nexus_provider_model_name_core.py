"""Tier a2 — assimilated method 'NexusProvider.model_name'

Assimilated from: provider.py:392-393
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
    return "nexus-inference"

