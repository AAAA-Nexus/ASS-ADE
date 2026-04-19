# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/cancellation.py:25
# Component id: sy.source.ass_ade.cancel
__version__ = "0.1.0"

    def cancel(self) -> None:
        """Mark this context as cancelled."""
        with self._lock:
            self._cancelled = True
