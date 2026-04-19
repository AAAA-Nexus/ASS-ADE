# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskfilter.py:7
# Component id: mo.source.a2_mo_composites.taskfilter
from __future__ import annotations

__version__ = "0.1.0"

class TaskFilter:
    """Feature module for filtering tasks."""

    def __init__(self, task_manager: TaskManager):
        """Initialize with task manager."""
        self.manager = task_manager

    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high-priority and urgent tasks."""
        all_tasks = self.manager.list_all_tasks()
        return filter_tasks_by_priority(all_tasks, TaskPriority.HIGH)

    def get_overdue_tasks(self) -> List[Task]:
        """Get all non-done tasks (would check dates in real impl)."""
        all_tasks = self.manager.list_all_tasks()
        return filter_tasks_by_status(all_tasks, TaskStatus.TODO)

    def find_by_assignee(self, assignee: str) -> List[Task]:
        """Find all tasks assigned to a person."""
        all_tasks = self.manager.list_all_tasks()
        return [t for t in all_tasks if t.assignee == assignee]

    def find_by_tag(self, tag: str) -> List[Task]:
        """Find all tasks with a specific tag."""
        all_tasks = self.manager.list_all_tasks()
        return [t for t in all_tasks if tag in t.tags]
