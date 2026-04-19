# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_priority_distribution.py:7
# Component id: at.source.a1_at_functions.get_priority_distribution
from __future__ import annotations

__version__ = "0.1.0"

def get_priority_distribution(self) -> dict:
    """Get count of tasks by priority."""
    all_tasks = self.manager.list_all_tasks()
    distribution = {p: 0 for p in TaskPriority}
    for task in all_tasks:
        distribution[task.priority] += 1
    return distribution
