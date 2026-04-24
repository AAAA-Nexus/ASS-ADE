"""Tier a1 — assimilated function 'unique_source_roots'

Assimilated from: pipeline_book.py:45-52
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Any, Sequence

from ass_ade.a1_at_functions.conflict_detector import (


# --- assimilated symbol ---
def unique_source_roots(
    primary: Path | str,
    extra_source_roots: Sequence[Path | str] | None = None,
) -> list[Path]:
    """Return ``[primary, ...extras]`` as resolved paths (order preserved; primary first)."""
    root = Path(primary).resolve()
    extras = [Path(p).resolve() for p in (extra_source_roots or ())]
    return [root] + extras

