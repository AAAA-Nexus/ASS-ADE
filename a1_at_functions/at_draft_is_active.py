# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_nexussession.py:15
# Component id: at.source.ass_ade.is_active
__version__ = "0.1.0"

    def is_active(self) -> bool:
        return self._started and self.session_id is not None
