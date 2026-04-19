# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add_task.py:7
# Component id: at.source.a1_at_functions.add_task
from __future__ import annotations

__version__ = "0.1.0"

def add_task(self, task: Task) -> bool:
    """Add a task to the collection."""
    if not validate_task_id(task.id):
        return False
    if not validate_task_title(task.title):
        return False
    self.tasks[task.id] = task
    return True
