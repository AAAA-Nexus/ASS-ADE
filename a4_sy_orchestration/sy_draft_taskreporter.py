# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:175
# Component id: sy.source.ass_ade.taskreporter
from __future__ import annotations

__version__ = "0.1.0"

class TaskReporter:
    """Feature module for task reporting."""

    def __init__(self, task_manager: TaskManager):
        """Initialize with task manager."""
        self.manager = task_manager

    def generate_status_report(self) -> str:
        """Generate a human-readable status report."""
        stats = self.manager.get_statistics()
        return (
            f"Task Report:\n"
            f"  Total tasks: {stats['total']}\n"
            f"  Completion: {stats['completion_rate']:.1f}%\n"
            f"  By status: {stats['by_status']}"
        )

    def get_priority_distribution(self) -> dict:
        """Get count of tasks by priority."""
        all_tasks = self.manager.list_all_tasks()
        distribution = {p: 0 for p in TaskPriority}
        for task in all_tasks:
            distribution[task.priority] += 1
        return distribution

    def get_workload_by_assignee(self) -> dict:
        """Count tasks assigned to each person."""
        all_tasks = self.manager.list_all_tasks()
        workload = {}
        for task in all_tasks:
            if task.assignee:
                workload[task.assignee] = workload.get(task.assignee, 0) + 1
        return workload
