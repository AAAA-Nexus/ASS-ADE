# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_absolute_private_ip_endpoint_raises.py:7
# Component id: at.source.a1_at_functions.test_absolute_private_ip_endpoint_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_absolute_private_ip_endpoint_raises(self) -> None:
    """Invoking a tool with private IP endpoint should raise ValueError."""
    from ass_ade.mcp.utils import invoke_tool

    tool = MCPTool(
        name="internal-tool",
        endpoint="https://192.168.1.1/internal",
        method="GET",
        paid=False,
    )

    with pytest.raises(ValueError, match="private/loopback address"):
        invoke_tool("https://api.example.com", tool)
