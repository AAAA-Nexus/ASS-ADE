# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:56
# Component id: qk.source.ass_ade.test_extended_tools_have_schemas
from __future__ import annotations

__version__ = "0.1.0"

def test_extended_tools_have_schemas(self) -> None:
    for tool in _WORKFLOW_TOOLS:
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool
        assert tool["inputSchema"]["type"] == "object"
        assert "required" in tool["inputSchema"]
