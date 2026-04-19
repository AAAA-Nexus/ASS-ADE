# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_conversation.py:31
# Component id: at.source.ass_ade.add_tool_result
__version__ = "0.1.0"

    def add_tool_result(self, tool_call_id: str, name: str, content: str) -> None:
        self._messages.append(
            Message(
                role="tool",
                content=content,
                tool_call_id=tool_call_id,
                name=name,
            )
        )
