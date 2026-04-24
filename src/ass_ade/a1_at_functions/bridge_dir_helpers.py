"""Tier a1 — assimilated function 'bridge_dir'

Assimilated from: rebuild/bridge_manifest.py:16-18
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# --- assimilated symbol ---
def bridge_dir(root: Path) -> Path:
    """Return the emitted bridge-control directory under a rebuild root."""
    return root / _BRIDGE_DIR_REL

