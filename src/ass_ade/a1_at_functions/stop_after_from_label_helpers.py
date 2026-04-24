"""Tier a1 — assimilated function 'stop_after_from_label'

Assimilated from: pipeline_book.py:55-61
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
def stop_after_from_label(label: str) -> int:
    """Resolve CLI / config label to terminal phase index (0–7)."""
    key = (label or "").strip().lower()
    if key not in STOP_AFTER_PHASE:
        allowed = ", ".join(sorted(STOP_AFTER_PHASE))
        raise ValueError(f"Unknown stop-after {label!r}; expected one of: {allowed}")
    return STOP_AFTER_PHASE[key]

