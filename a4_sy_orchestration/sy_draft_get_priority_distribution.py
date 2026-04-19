# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:192
# Component id: sy.source.ass_ade.get_priority_distribution
from __future__ import annotations

__version__ = "0.1.0"

def get_priority_distribution(self) -> dict:
    """Get count of tasks by priority."""
    all_tasks = self.manager.list_all_tasks()
    distribution = {p: 0 for p in TaskPriority}
    for task in all_tasks:
        distribution[task.priority] += 1
    return distribution
