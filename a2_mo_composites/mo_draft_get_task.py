# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:23
# Component id: mo.source.a2_mo_composites.get_task
from __future__ import annotations

__version__ = "0.1.0"

def get_task(self, task_id: str) -> Optional[Task]:
    """Retrieve a task by ID."""
    return self.tasks.get(task_id)
