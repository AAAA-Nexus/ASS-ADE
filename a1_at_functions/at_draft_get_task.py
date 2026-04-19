# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_task.py:7
# Component id: at.source.a1_at_functions.get_task
from __future__ import annotations

__version__ = "0.1.0"

def get_task(self, task_id: str) -> Optional[Task]:
    """Retrieve a task by ID."""
    return self.tasks.get(task_id)
