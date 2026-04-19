# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_sort_tasks_by_priority.py:7
# Component id: at.source.a1_at_functions.sort_tasks_by_priority
from __future__ import annotations

__version__ = "0.1.0"

def sort_tasks_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority (pure function)."""
    return sorted(tasks, key=lambda t: t.priority.value, reverse=descending)
