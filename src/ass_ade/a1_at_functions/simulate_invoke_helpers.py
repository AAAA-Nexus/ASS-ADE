"""Tier a1 — assimilated function 'simulate_invoke'

Assimilated from: utils.py:97-119
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
def simulate_invoke(base_url: str, tool: MCPTool, payload: Any | None = None) -> dict:
    """Return a simulation summary of invoking the given tool without network I/O.

    The result is a JSON-serializable dict suitable for printing to users or
    CI systems when doing a dry-run. Absolute endpoints are validated for SSRF safety.
    Raises ValueError if an absolute endpoint fails validation.
    """
    endpoint = tool.endpoint or ""
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        # Absolute endpoint: validate for SSRF safety
        url = _validate_absolute_endpoint(endpoint)
    else:
        url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")

    return {
        "simulated": True,
        "tool": tool.name,
        "method": (tool.method or "POST").upper(),
        "endpoint": url,
        "paid": bool(tool.paid),
        "payload_preview": payload,
        "note": "dry-run; no network request performed",
    }

