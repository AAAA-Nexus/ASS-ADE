# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_add_tool_result.py:7
# Component id: at.source.a1_at_functions.test_add_tool_result
from __future__ import annotations

__version__ = "0.1.0"

def test_add_tool_result(self):
    c = Conversation()
    c.add_tool_result("c1", "read_file", "file data")
    m = c.messages[-1]
    assert m.role == "tool"
    assert m.tool_call_id == "c1"
    assert m.name == "read_file"
