# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_taskstatus.py:7
# Component id: mo.source.a2_mo_composites.taskstatus
from __future__ import annotations

__version__ = "0.1.0"

class TaskStatus(Enum):
    """Task state constants."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
