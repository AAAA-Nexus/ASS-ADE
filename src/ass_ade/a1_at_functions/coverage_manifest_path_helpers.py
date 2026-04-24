"""Tier a1 — assimilated function 'coverage_manifest_path'

Assimilated from: rebuild/coverage_manifest.py:28-31
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal


# --- assimilated symbol ---
def coverage_manifest_path(root: Path, kind: CoverageKind) -> Path:
    """Return the manifest path for the requested coverage artifact kind."""
    filename = _TEST_MANIFEST_NAME if kind == "test" else _DOC_MANIFEST_NAME
    return coverage_dir(root) / filename

