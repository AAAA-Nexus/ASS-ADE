# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_task_id.py:7
# Component id: at.source.a1_at_functions.validate_task_id
from __future__ import annotations

__version__ = "0.1.0"

def validate_task_id(task_id: str) -> bool:
    """Check if task ID is valid (pure function)."""
    return bool(task_id) and len(task_id) <= 50
