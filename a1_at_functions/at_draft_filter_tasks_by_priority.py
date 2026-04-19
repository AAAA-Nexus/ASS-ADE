# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_filter_tasks_by_priority.py:5
# Component id: at.source.ass_ade.filter_tasks_by_priority
__version__ = "0.1.0"

def filter_tasks_by_priority(tasks: List[Task], min_priority: TaskPriority) -> List[Task]:
    """Filter tasks by minimum priority (pure function)."""
    return [t for t in tasks if t.priority.value >= min_priority.value]
