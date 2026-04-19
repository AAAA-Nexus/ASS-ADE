# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_minimal.py:7
# Component id: at.source.a1_at_functions.test_minimal
from __future__ import annotations

__version__ = "0.1.0"

def test_minimal(self):
    m = Message(role="user", content="hello")
    assert m.role == "user"
    assert m.content == "hello"
    assert m.tool_calls == []
    assert m.tool_call_id is None
