# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:74
# Component id: sy.source.ass_ade.count_tasks_by_status
__version__ = "0.1.0"

def count_tasks_by_status(tasks: List[Task]) -> dict:
    """Count tasks in each status (pure function)."""
    counts = {status: 0 for status in TaskStatus}
    for task in tasks:
        counts[task.status] += 1
    return counts
