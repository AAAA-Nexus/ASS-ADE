# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatetoolstokens.py:20
# Component id: qk.source.a0_qk_constants.test_multiple_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_multiple_tools(self):
    tools = [
        ToolSchema(name=f"tool_{i}", description=f"Tool number {i}", parameters={"type": "object"})
        for i in range(5)
    ]
    tokens = estimate_tools_tokens(tools)
    assert tokens > estimate_tools_tokens(tools[:1])
