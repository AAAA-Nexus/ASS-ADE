# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_conversation.py:25
# Component id: at.source.ass_ade.add_user
__version__ = "0.1.0"

    def add_user(self, content: str) -> None:
        self._messages.append(Message(role="user", content=content))
