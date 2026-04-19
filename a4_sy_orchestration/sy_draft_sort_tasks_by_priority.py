# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:69
# Component id: sy.source.ass_ade.sort_tasks_by_priority
__version__ = "0.1.0"

def sort_tasks_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority (pure function)."""
    return sorted(tasks, key=lambda t: t.priority.value, reverse=descending)
