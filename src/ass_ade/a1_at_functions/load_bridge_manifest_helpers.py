"""Tier a1 — assimilated function 'load_bridge_manifest'

Assimilated from: rebuild/bridge_manifest.py:26-36
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# --- assimilated symbol ---
def load_bridge_manifest(root: Path) -> dict[str, Any] | None:
    """Load an emitted multi-language bridge manifest when it is valid."""
    path = bridge_manifest_path(root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if payload.get("schema") != MULTILANG_BRIDGE_SCHEMA:
        return None
    return payload

