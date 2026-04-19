# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_update_task_status.py:7
# Component id: at.source.a1_at_functions.update_task_status
from __future__ import annotations

__version__ = "0.1.0"

def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
    """Update a task's status."""
    task = self.get_task(task_id)
    if task:
        task.status = new_status
        return True
    return False
