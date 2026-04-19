# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:69
# Component id: sy.source.ass_ade.sort_tasks_by_priority
from __future__ import annotations

__version__ = "0.1.0"

def sort_tasks_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority (pure function)."""
    return sorted(tasks, key=lambda t: t.priority.value, reverse=descending)
