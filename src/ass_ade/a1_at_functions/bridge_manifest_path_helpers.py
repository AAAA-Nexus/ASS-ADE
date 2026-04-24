"""Tier a1 — assimilated function 'bridge_manifest_path'

Assimilated from: rebuild/bridge_manifest.py:21-23
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# --- assimilated symbol ---
def bridge_manifest_path(root: Path) -> Path:
    """Return the emitted multi-language bridge manifest path."""
    return bridge_dir(root) / _BRIDGE_MANIFEST_NAME

