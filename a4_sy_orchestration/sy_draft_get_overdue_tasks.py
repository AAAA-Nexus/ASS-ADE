# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:159
# Component id: sy.source.ass_ade.get_overdue_tasks
from __future__ import annotations

__version__ = "0.1.0"

def get_overdue_tasks(self) -> List[Task]:
    """Get all non-done tasks (would check dates in real impl)."""
    all_tasks = self.manager.list_all_tasks()
    return filter_tasks_by_status(all_tasks, TaskStatus.TODO)
