# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_nullcancellationcontext.py:5
# Component id: mo.source.ass_ade.nullcancellationcontext
__version__ = "0.1.0"

class NullCancellationContext(CancellationContext):
    """No-op cancellation context for operations that don't support cancellation."""

    def cancel(self) -> None:
        """Do nothing."""
        pass

    def check(self) -> bool:
        """Always return False — never cancelled."""
        return False
