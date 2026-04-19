# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_find_by_tag.py:7
# Component id: at.source.a1_at_functions.find_by_tag
from __future__ import annotations

__version__ = "0.1.0"

def find_by_tag(self, tag: str) -> List[Task]:
    """Find all tasks with a specific tag."""
    all_tasks = self.manager.list_all_tasks()
    return [t for t in all_tasks if tag in t.tags]
