"""Tier a1 — assimilated function 'episodes_jsonl_path'

Assimilated from: rebuild/autopoiesis_layout.py:30-32
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path

from ass_ade.engine.rebuild.autopoiesis_constants import (


# --- assimilated symbol ---
def episodes_jsonl_path(repo_root: Path) -> Path:
    """Return path to the append-only Forge / autopoiesis episode log."""
    return autopoiesis_memory_root(repo_root) / MEMORY_EPISODES_FILE

