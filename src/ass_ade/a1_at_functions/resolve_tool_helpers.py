"""Tier a1 — assimilated function 'resolve_tool'

Assimilated from: utils.py:23-38
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
def resolve_tool(manifest: MCPManifest, identifier: str) -> MCPTool | None:
    """Resolve a tool by index (1-based) or name.

    identifier may be a numeric string referencing the manifest list index,
    or a tool name.
    """
    if identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(manifest.tools):
            return manifest.tools[idx]
        return None

    for tool in manifest.tools:
        if tool.name and tool.name.lower() == identifier.lower():
            return tool
    return None

