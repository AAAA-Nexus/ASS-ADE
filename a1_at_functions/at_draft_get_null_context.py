# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_get_null_context.py:5
# Component id: at.source.ass_ade.get_null_context
__version__ = "0.1.0"

def get_null_context() -> CancellationContext:
    """Get a singleton no-op cancellation context."""
    return NullCancellationContext()
