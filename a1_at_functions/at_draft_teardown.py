# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_nexussession.py:64
# Component id: at.source.ass_ade.teardown
__version__ = "0.1.0"

    def teardown(self) -> None:
        """Mark the session as ended (client-side only)."""
        self.session_id = None
        self.epoch = 0
        self._started = False
