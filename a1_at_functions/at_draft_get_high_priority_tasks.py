# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_high_priority_tasks.py:7
# Component id: at.source.a1_at_functions.get_high_priority_tasks
from __future__ import annotations

__version__ = "0.1.0"

def get_high_priority_tasks(self) -> List[Task]:
    """Get all high-priority and urgent tasks."""
    all_tasks = self.manager.list_all_tasks()
    return filter_tasks_by_priority(all_tasks, TaskPriority.HIGH)
