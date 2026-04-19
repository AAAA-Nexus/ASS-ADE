# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:17
# Component id: sy.source.ass_ade.taskstatus
from __future__ import annotations

__version__ = "0.1.0"

class TaskStatus(Enum):
    """Task state constants."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
