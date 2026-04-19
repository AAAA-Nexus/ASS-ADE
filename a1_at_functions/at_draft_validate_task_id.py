# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_validate_task_id.py:5
# Component id: at.source.ass_ade.validate_task_id
__version__ = "0.1.0"

def validate_task_id(task_id: str) -> bool:
    """Check if task ID is valid (pure function)."""
    return bool(task_id) and len(task_id) <= 50
