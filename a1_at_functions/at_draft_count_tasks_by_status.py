# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_count_tasks_by_status.py:7
# Component id: at.source.a1_at_functions.count_tasks_by_status
from __future__ import annotations

__version__ = "0.1.0"

def count_tasks_by_status(tasks: List[Task]) -> dict:
    """Count tasks in each status (pure function)."""
    counts = {status: 0 for status in TaskStatus}
    for task in tasks:
        counts[task.status] += 1
    return counts
