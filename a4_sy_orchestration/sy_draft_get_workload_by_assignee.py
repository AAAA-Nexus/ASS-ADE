# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:200
# Component id: sy.source.ass_ade.get_workload_by_assignee
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
