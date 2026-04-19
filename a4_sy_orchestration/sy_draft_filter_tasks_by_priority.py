# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:59
# Component id: sy.source.ass_ade.filter_tasks_by_priority
from __future__ import annotations

__version__ = "0.1.0"

def filter_tasks_by_priority(tasks: List[Task], min_priority: TaskPriority) -> List[Task]:
    """Filter tasks by minimum priority (pure function)."""
    return [t for t in tasks if t.priority.value >= min_priority.value]
