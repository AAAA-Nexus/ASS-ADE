# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:49
# Component id: at.source.ass_ade.validate_task_title
from __future__ import annotations

__version__ = "0.1.0"

def validate_task_title(title: str) -> bool:
    """Check if task title is valid (pure function)."""
    return bool(title) and 1 <= len(title) <= 255
