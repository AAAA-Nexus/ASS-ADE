# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_list_all_tasks.py:7
# Component id: at.source.a1_at_functions.list_all_tasks
from __future__ import annotations

__version__ = "0.1.0"

def list_all_tasks(self) -> List[Task]:
    """Get all tasks."""
    return list(self.tasks.values())
