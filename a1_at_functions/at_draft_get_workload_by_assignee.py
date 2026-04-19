# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_workload_by_assignee.py:7
# Component id: at.source.a1_at_functions.get_workload_by_assignee
from __future__ import annotations

__version__ = "0.1.0"

def get_workload_by_assignee(self) -> dict:
    """Count tasks assigned to each person."""
    all_tasks = self.manager.list_all_tasks()
    workload = {}
    for task in all_tasks:
        if task.assignee:
            workload[task.assignee] = workload.get(task.assignee, 0) + 1
    return workload
