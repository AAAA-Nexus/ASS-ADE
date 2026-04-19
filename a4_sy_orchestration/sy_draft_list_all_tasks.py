# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:121
# Component id: sy.source.ass_ade.list_all_tasks
from __future__ import annotations

__version__ = "0.1.0"

def list_all_tasks(self) -> List[Task]:
    """Get all tasks."""
    return list(self.tasks.values())
