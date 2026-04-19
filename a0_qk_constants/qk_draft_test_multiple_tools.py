# Extracted from C:/!ass-ade/tests/test_tokens.py:85
# Component id: qk.source.ass_ade.test_multiple_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_multiple_tools(self):
    tools = [
        ToolSchema(name=f"tool_{i}", description=f"Tool number {i}", parameters={"type": "object"})
        for i in range(5)
    ]
    tokens = estimate_tools_tokens(tools)
    assert tokens > estimate_tools_tokens(tools[:1])
