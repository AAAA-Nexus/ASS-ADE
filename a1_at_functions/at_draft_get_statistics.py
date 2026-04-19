# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_statistics.py:7
# Component id: at.source.a1_at_functions.get_statistics
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
