# Extracted from C:/!ass-ade/tests/test_tokens.py:76
# Component id: qk.source.ass_ade.test_single_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_single_tool(self):
    tool = ToolSchema(
        name="read_file",
        description="Read a file",
        parameters={"type": "object", "properties": {"path": {"type": "string"}}},
    )
    tokens = estimate_tools_tokens([tool])
    assert tokens > 0
