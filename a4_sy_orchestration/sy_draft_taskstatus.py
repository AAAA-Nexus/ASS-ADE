# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:17
# Component id: sy.source.ass_ade.taskstatus
__version__ = "0.1.0"

class TaskStatus(Enum):
    """Task state constants."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
