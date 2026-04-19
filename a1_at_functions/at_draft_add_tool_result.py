# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add_tool_result.py:7
# Component id: at.source.a1_at_functions.add_tool_result
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
