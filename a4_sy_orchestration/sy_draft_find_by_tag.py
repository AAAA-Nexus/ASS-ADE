# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:169
# Component id: sy.source.ass_ade.find_by_tag
from __future__ import annotations

__version__ = "0.1.0"

def find_by_tag(self, tag: str) -> List[Task]:
    """Find all tasks with a specific tag."""
    all_tasks = self.manager.list_all_tasks()
    return [t for t in all_tasks if tag in t.tags]
