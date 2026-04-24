"""Tier a1 — assimilated function 'validate_payload'

Assimilated from: utils.py:132-148
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
def validate_payload(schema: dict | None, payload: Any | None) -> tuple[bool, str | None]:
    """Validate the given payload against the provided JSON Schema.

    Returns (True, None) when valid, otherwise (False, error_message).
    """
    if schema is None:
        return True, None

    try:
        # jsonschema expects a concrete instance; use None -> {} for convenience
        instance = payload if payload is not None else {}
        jsonschema.validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as exc:
        return False, str(exc)
    except jsonschema.SchemaError as exc:
        return False, f"schema validation error: {exc}"

