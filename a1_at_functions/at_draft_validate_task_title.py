# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_task_title.py:7
# Component id: at.source.a1_at_functions.validate_task_title
from __future__ import annotations

__version__ = "0.1.0"

def validate_task_title(title: str) -> bool:
    """Check if task title is valid (pure function)."""
    return bool(title) and 1 <= len(title) <= 255
