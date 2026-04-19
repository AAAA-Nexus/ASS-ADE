# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_filter_tasks_by_status.py:5
# Component id: at.source.ass_ade.filter_tasks_by_status
__version__ = "0.1.0"

def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status (pure function)."""
    return [t for t in tasks if t.status == status]
