# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_filter_tasks_by_priority.py:7
# Component id: at.source.a1_at_functions.filter_tasks_by_priority
from __future__ import annotations

__version__ = "0.1.0"

def filter_tasks_by_priority(tasks: List[Task], min_priority: TaskPriority) -> List[Task]:
    """Filter tasks by minimum priority (pure function)."""
    return [t for t in tasks if t.priority.value >= min_priority.value]
