# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_conversation.py:48
# Component id: at.source.ass_ade.trim
__version__ = "0.1.0"

    def trim(self, max_messages: int = 50) -> int:
        """Trim oldest non-system messages if over limit. Returns count removed."""
        if len(self._messages) <= max_messages:
            return 0

        system = [m for m in self._messages if m.role == "system"]
        others = [m for m in self._messages if m.role != "system"]

        keep = max_messages - len(system)
        removed = len(others) - keep
        if removed <= 0:
            return 0

        self._messages = system + others[removed:]
        return removed
