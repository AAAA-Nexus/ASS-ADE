"""Tier a1 — assimilated function 'autopoiesis_memory_root'

Assimilated from: rebuild/autopoiesis_layout.py:16-21
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path

from ass_ade.engine.rebuild.autopoiesis_constants import (


# --- assimilated symbol ---
def autopoiesis_memory_root(repo_root: Path) -> Path:
    """Return ``<repo>/.ass-ade/memory`` as a path object."""
    base = repo_root
    for part in MEMORY_ROOT_REL:
        base /= part
    return base

