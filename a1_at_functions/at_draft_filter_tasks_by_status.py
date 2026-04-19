# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_filter_tasks_by_status.py:7
# Component id: at.source.a1_at_functions.filter_tasks_by_status
from __future__ import annotations

__version__ = "0.1.0"

def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status (pure function)."""
    return [t for t in tasks if t.status == status]
