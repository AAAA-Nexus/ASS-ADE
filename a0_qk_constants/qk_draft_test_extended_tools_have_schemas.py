# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_extended_tools_have_schemas.py:7
# Component id: qk.source.a0_qk_constants.test_extended_tools_have_schemas
from __future__ import annotations

__version__ = "0.1.0"

def test_extended_tools_have_schemas(self) -> None:
    for tool in _WORKFLOW_TOOLS:
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool
        assert tool["inputSchema"]["type"] == "object"
        assert "required" in tool["inputSchema"]
