# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_count_tasks_by_status.py:5
# Component id: at.source.ass_ade.count_tasks_by_status
__version__ = "0.1.0"

def count_tasks_by_status(tasks: List[Task]) -> dict:
    """Count tasks in each status (pure function)."""
    counts = {status: 0 for status in TaskStatus}
    for task in tasks:
        counts[task.status] += 1
    return counts
