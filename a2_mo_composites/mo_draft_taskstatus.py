# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskstatus.py:5
# Component id: mo.source.ass_ade.taskstatus
__version__ = "0.1.0"

class TaskStatus(Enum):
    """Task state constants."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
