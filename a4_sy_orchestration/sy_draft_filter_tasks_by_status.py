# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:64
# Component id: sy.source.ass_ade.filter_tasks_by_status
__version__ = "0.1.0"

def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status (pure function)."""
    return [t for t in tasks if t.status == status]
