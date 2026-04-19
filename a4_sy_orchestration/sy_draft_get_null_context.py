# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/cancellation.py:58
# Component id: sy.source.ass_ade.get_null_context
__version__ = "0.1.0"

def get_null_context() -> CancellationContext:
    """Get a singleton no-op cancellation context."""
    return NullCancellationContext()
