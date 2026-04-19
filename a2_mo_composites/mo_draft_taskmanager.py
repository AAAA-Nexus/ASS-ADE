# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:7
# Component id: mo.source.a2_mo_composites.taskmanager
from __future__ import annotations

__version__ = "0.1.0"

class TaskManager:
    """Manages task collection and state."""

    def __init__(self):
        """Initialize empty task collection."""
        self.tasks: dict[str, Task] = {}

    def add_task(self, task: Task) -> bool:
        """Add a task to the collection."""
        if not validate_task_id(task.id):
            return False
        if not validate_task_title(task.title):
            return False
        self.tasks[task.id] = task
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
        """Update a task's status."""
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def list_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def get_statistics(self) -> dict:
        """Get task statistics."""
        all_tasks = self.list_all_tasks()
        return {
            "total": len(all_tasks),
            "by_status": count_tasks_by_status(all_tasks),
            "completion_rate": self._calculate_completion_rate(all_tasks),
        }

    @staticmethod
    def _calculate_completion_rate(tasks: List[Task]) -> float:
        """Calculate completion percentage (static helper)."""
        if not tasks:
            return 0.0
        done = sum(1 for t in tasks if t.status == TaskStatus.DONE)
        return (done / len(tasks)) * 100
