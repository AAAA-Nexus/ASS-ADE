# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:42
# Component id: mo.source.a2_mo_composites.list_all_tasks
from __future__ import annotations

__version__ = "0.1.0"

def list_all_tasks(self) -> List[Task]:
    """Get all tasks."""
    return list(self.tasks.values())
