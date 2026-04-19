# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_conversation.py:44
# Component id: qk.source.ass_ade.estimated_tokens
__version__ = "0.1.0"

    def estimated_tokens(self) -> int:
        """Total estimated tokens across all messages."""
        return sum(estimate_message_tokens(m) for m in self._messages)
