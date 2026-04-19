# Extracted from C:/!ass-ade/tests/test_agent.py:35
# Component id: at.source.ass_ade.test_add_tool_result
from __future__ import annotations

__version__ = "0.1.0"

def test_add_tool_result(self):
    c = Conversation()
    c.add_tool_result("c1", "read_file", "file data")
    m = c.messages[-1]
    assert m.role == "tool"
    assert m.tool_call_id == "c1"
    assert m.name == "read_file"
