# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_with_tool_calls.py:7
# Component id: at.source.a1_at_functions.test_with_tool_calls
from __future__ import annotations

__version__ = "0.1.0"

def test_with_tool_calls(self):
    tc = ToolCallRequest(id="c1", name="read_file", arguments={"path": "a.py"})
    m = Message(role="assistant", content="", tool_calls=[tc])
    assert len(m.tool_calls) == 1
    assert m.tool_calls[0].name == "read_file"
