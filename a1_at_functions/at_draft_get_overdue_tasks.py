# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_overdue_tasks.py:7
# Component id: at.source.a1_at_functions.get_overdue_tasks
from __future__ import annotations

__version__ = "0.1.0"

def get_overdue_tasks(self) -> List[Task]:
    """Get all non-done tasks (would check dates in real impl)."""
    all_tasks = self.manager.list_all_tasks()
    return filter_tasks_by_status(all_tasks, TaskStatus.TODO)
