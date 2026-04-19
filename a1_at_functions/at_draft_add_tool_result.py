# Extracted from C:/!ass-ade/src/ass_ade/agent/conversation.py:44
# Component id: at.source.ass_ade.add_tool_result
from __future__ import annotations

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
