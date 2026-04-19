# Extracted from C:/!ass-ade/examples/02-rebuild-a-codebase/sample_project/main.py:25
# Component id: sy.source.ass_ade.taskpriority
from __future__ import annotations

__version__ = "0.1.0"

class TaskPriority(Enum):
    """Priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
