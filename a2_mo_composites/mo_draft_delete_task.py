# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:35
# Component id: mo.source.a2_mo_composites.delete_task
from __future__ import annotations

__version__ = "0.1.0"

def delete_task(self, task_id: str) -> bool:
    """Delete a task."""
    if task_id in self.tasks:
        del self.tasks[task_id]
        return True
    return False
