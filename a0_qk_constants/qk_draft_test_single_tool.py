# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatetoolstokens.py:11
# Component id: qk.source.a0_qk_constants.test_single_tool
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
