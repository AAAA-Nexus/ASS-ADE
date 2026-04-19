# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:34
# Component id: sy.source.ass_ade.task
from __future__ import annotations

__version__ = "0.1.0"

class Task:
    """Task data structure."""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)
