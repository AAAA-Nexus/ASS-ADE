# Extracted from C:/!ass-ade/tests/test_engine.py:38
# Component id: mo.source.ass_ade.test_tool_result
from __future__ import annotations

__version__ = "0.1.0"

def test_tool_result(self):
    m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
    assert m.role == "tool"
    assert m.tool_call_id == "c1"
