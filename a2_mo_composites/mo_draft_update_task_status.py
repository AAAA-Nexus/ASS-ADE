# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:27
# Component id: mo.source.a2_mo_composites.update_task_status
from __future__ import annotations

__version__ = "0.1.0"

def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
    """Update a task's status."""
    task = self.get_task(task_id)
    if task:
        task.status = new_status
        return True
    return False
