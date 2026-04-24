"""Tier a1 — assimilated function 'coverage_dir'

Assimilated from: rebuild/coverage_manifest.py:23-25
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal


# --- assimilated symbol ---
def coverage_dir(root: Path) -> Path:
    """Return the coverage artifact directory under a rebuild root."""
    return root / _COVERAGE_DIR_REL

