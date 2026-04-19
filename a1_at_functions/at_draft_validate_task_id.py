# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:54
# Component id: at.source.ass_ade.validate_task_id
from __future__ import annotations

__version__ = "0.1.0"

def validate_task_id(task_id: str) -> bool:
    """Check if task ID is valid (pure function)."""
    return bool(task_id) and len(task_id) <= 50
