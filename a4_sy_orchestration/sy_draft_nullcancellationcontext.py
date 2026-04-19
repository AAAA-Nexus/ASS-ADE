# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/cancellation.py:46
# Component id: sy.source.ass_ade.nullcancellationcontext
__version__ = "0.1.0"

class NullCancellationContext(CancellationContext):
    """No-op cancellation context for operations that don't support cancellation."""

    def cancel(self) -> None:
        """Do nothing."""
        pass

    def check(self) -> bool:
        """Always return False — never cancelled."""
        return False
