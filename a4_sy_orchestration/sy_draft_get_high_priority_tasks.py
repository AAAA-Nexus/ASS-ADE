# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:154
# Component id: sy.source.ass_ade.get_high_priority_tasks
from __future__ import annotations

__version__ = "0.1.0"

def get_high_priority_tasks(self) -> List[Task]:
    """Get all high-priority and urgent tasks."""
    all_tasks = self.manager.list_all_tasks()
    return filter_tasks_by_priority(all_tasks, TaskPriority.HIGH)
