"""Tier a1 — assimilated function 'estimate_cost'

Assimilated from: utils.py:122-129
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import time
from typing import Any

import httpx
import jsonschema
from jsonschema import ValidationError

from ass_ade.nexus.models import CostEstimate, MCPManifest, MCPTool
from ass_ade.nexus.validation import sanitize_header_value, validate_https_public_url


# --- assimilated symbol ---
def estimate_cost(tool: MCPTool) -> CostEstimate | None:
    """Return the cost metadata for a tool, or None if the tool is free / metadata unavailable."""
    if tool.cost is not None:
        return tool.cost
    if bool(tool.paid):
        # Manifest declares paid but no cost detail; return a placeholder.
        return CostEstimate(notes="paid tool – no cost detail in manifest")
    return None

