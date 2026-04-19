# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_delete_task.py:7
# Component id: at.source.a1_at_functions.delete_task
from __future__ import annotations

__version__ = "0.1.0"

def delete_task(self, task_id: str) -> bool:
    """Delete a task."""
    if task_id in self.tasks:
        del self.tasks[task_id]
        return True
    return False
