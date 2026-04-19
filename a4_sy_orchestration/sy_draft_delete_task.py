# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:114
# Component id: sy.source.ass_ade.delete_task
from __future__ import annotations

__version__ = "0.1.0"

def delete_task(self, task_id: str) -> bool:
    """Delete a task."""
    if task_id in self.tasks:
        del self.tasks[task_id]
        return True
    return False
