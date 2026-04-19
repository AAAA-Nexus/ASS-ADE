# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_cancellationcontext.py:17
# Component id: at.source.ass_ade.cancel
__version__ = "0.1.0"

    def cancel(self) -> None:
        """Mark this context as cancelled."""
        with self._lock:
            self._cancelled = True
