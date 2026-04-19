# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_task.py:7
# Component id: mo.source.a2_mo_composites.task
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
