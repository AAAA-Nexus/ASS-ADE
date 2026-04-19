# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testmessage.py:7
# Component id: mo.source.a2_mo_composites.testmessage
from __future__ import annotations

__version__ = "0.1.0"

class TestMessage:
    def test_minimal(self):
        m = Message(role="user", content="hello")
        assert m.role == "user"
        assert m.content == "hello"
        assert m.tool_calls == []
        assert m.tool_call_id is None

    def test_with_tool_calls(self):
        tc = ToolCallRequest(id="c1", name="read_file", arguments={"path": "a.py"})
        m = Message(role="assistant", content="", tool_calls=[tc])
        assert len(m.tool_calls) == 1
        assert m.tool_calls[0].name == "read_file"

    def test_tool_result(self):
        m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
        assert m.role == "tool"
        assert m.tool_call_id == "c1"
