# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskmanager.py:46
# Component id: mo.source.a2_mo_composites.get_statistics
from __future__ import annotations

__version__ = "0.1.0"

def get_statistics(self) -> dict:
    """Get task statistics."""
    all_tasks = self.list_all_tasks()
    return {
        "total": len(all_tasks),
        "by_status": count_tasks_by_status(all_tasks),
        "completion_rate": self._calculate_completion_rate(all_tasks),
    }
