"""Tier a1 — assimilated function 'iter_autopoiesis_topic_paths'

Assimilated from: rebuild/autopoiesis_layout.py:24-27
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path

from ass_ade.engine.rebuild.autopoiesis_constants import (


# --- assimilated symbol ---
def iter_autopoiesis_topic_paths(repo_root: Path) -> tuple[Path, ...]:
    """Return topic shard paths (codebase, user, workspace, memory)."""
    root = autopoiesis_memory_root(repo_root)
    return tuple(root / name for name in AUTOPOIESIS_TOPICS)

