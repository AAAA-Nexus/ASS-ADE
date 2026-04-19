# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcptoolendpointssrf.py:10
# Component id: sy.source.a4_sy_orchestration.test_absolute_localhost_endpoint_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_absolute_localhost_endpoint_raises(self) -> None:
    """Invoking a tool with localhost endpoint should raise ValueError."""
    from ass_ade.mcp.utils import invoke_tool

    tool = MCPTool(
        name="admin-tool",
        endpoint="https://localhost:8080/admin",
        method="POST",
        paid=False,
    )

    with pytest.raises(ValueError, match="blocked network address|localhost"):
        invoke_tool("https://api.example.com", tool)
