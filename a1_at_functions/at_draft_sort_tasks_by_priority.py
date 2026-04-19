# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_sort_tasks_by_priority.py:5
# Component id: at.source.ass_ade.sort_tasks_by_priority
__version__ = "0.1.0"

def sort_tasks_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority (pure function)."""
    return sorted(tasks, key=lambda t: t.priority.value, reverse=descending)
