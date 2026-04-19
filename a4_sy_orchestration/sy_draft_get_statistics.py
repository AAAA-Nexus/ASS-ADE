# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:125
# Component id: sy.source.ass_ade.get_statistics
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
