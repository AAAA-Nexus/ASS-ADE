# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:64
# Component id: sy.source.ass_ade.filter_tasks_by_status
from __future__ import annotations

__version__ = "0.1.0"

def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status (pure function)."""
    return [t for t in tasks if t.status == status]
