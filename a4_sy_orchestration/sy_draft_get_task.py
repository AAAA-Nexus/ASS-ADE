# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:102
# Component id: sy.source.ass_ade.get_task
from __future__ import annotations

__version__ = "0.1.0"

def get_task(self, task_id: str) -> Optional[Task]:
    """Retrieve a task by ID."""
    return self.tasks.get(task_id)
