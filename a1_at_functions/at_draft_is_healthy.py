# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_nexussession.py:53
# Component id: at.source.ass_ade.is_healthy
__version__ = "0.1.0"

    def is_healthy(self) -> bool:
        """Return True if the session is active and has remaining calls."""
        if not self.is_active:
            return False
        try:
            s = self.status()
            remaining = s.remaining_calls
            return remaining is None or remaining > 0
        except NexusError:
            return False
