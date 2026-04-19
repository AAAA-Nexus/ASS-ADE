# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tool_result.py:7
# Component id: at.source.a1_at_functions.test_tool_result
from __future__ import annotations

__version__ = "0.1.0"

def test_tool_result(self):
    m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
    assert m.role == "tool"
    assert m.tool_call_id == "c1"
