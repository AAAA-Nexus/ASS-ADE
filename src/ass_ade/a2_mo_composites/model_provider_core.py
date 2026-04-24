"""Tier a2 — assimilated class 'ModelProvider'

Assimilated from: provider.py:21-24
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
class ModelProvider(Protocol):
    """Protocol for LLM providers."""

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...

