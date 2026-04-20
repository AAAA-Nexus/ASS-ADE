"""
Sample task manager demonstrating ASS-ADE rebuild tiers.

This is a toy project to show rebuild engine output.
It's not meant to be run — just to be analyzed.
"""

# ============================================================================
# Tier 1: qk_codex (Constants and Type Definitions)
# ============================================================================

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class TaskStatus(Enum):
    """Task state constants."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Task data structure."""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)


# ============================================================================
# Tier 2: at_kernel (Pure Functions)
# ============================================================================

def validate_task_title(title: str) -> bool:
    """Check if task title is valid (pure function)."""
    return bool(title) and 1 <= len(title) <= 255


def validate_task_id(task_id: str) -> bool:
    """Check if task ID is valid (pure function)."""
    return bool(task_id) and len(task_id) <= 50


def filter_tasks_by_priority(tasks: List[Task], min_priority: TaskPriority) -> List[Task]:
    """Filter tasks by minimum priority (pure function)."""
    return [t for t in tasks if t.priority.value >= min_priority.value]


def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status (pure function)."""
    return [t for t in tasks if t.status == status]


def sort_tasks_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority (pure function)."""
    return sorted(tasks, key=lambda t: t.priority.value, reverse=descending)


def count_tasks_by_status(tasks: List[Task]) -> dict:
    """Count tasks in each status (pure function)."""
    counts = {status: 0 for status in TaskStatus}
    for task in tasks:
        counts[task.status] += 1
    return counts


# ============================================================================
# Tier 3: mo_engines (Stateful Classes)
# ============================================================================

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


# ============================================================================
# Tier 4: og_swarm (Feature Modules)
# ============================================================================

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


# ============================================================================
# Tier 5: sy_manifold (Orchestration)
# ============================================================================

# In a real application, main() would be here.
# For this sample, we're just demonstrating the tier structure.
#
# Example orchestration:
#
#   def main():
#       manager = TaskManager()
#       filter_feature = TaskFilter(manager)
#       reporter = TaskReporter(manager)
#
#       # Add some tasks...
#       task = Task(id="t1", title="Fix bug")
#       manager.add_task(task)
#
#       # Use features...
#       print(reporter.generate_status_report())
#       high_priority = filter_feature.get_high_priority_tasks()
#
#   if __name__ == "__main__":
#       main()
