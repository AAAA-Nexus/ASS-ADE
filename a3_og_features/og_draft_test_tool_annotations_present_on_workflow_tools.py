# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:266
# Component id: og.source.ass_ade.test_tool_annotations_present_on_workflow_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_tool_annotations_present_on_workflow_tools(self) -> None:
    for tool in _WORKFLOW_TOOLS:
        assert "annotations" in tool, f"{tool['name']} missing annotations"
        ann = tool["annotations"]
        assert "readOnlyHint" in ann
        assert "destructiveHint" in ann
        assert "idempotentHint" in ann
        assert "openWorldHint" in ann
