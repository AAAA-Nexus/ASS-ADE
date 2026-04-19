# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcptoolendpointssrf.py:38
# Component id: sy.source.a4_sy_orchestration.test_relative_endpoint_uses_base_url
from __future__ import annotations

__version__ = "0.1.0"

def test_relative_endpoint_uses_base_url(self) -> None:
    """Relative endpoints should be joined to base_url without SSRF validation."""
    from ass_ade.mcp.utils import simulate_invoke

    tool = MCPTool(
        name="safe-tool",
        endpoint="/api/invoke",
        method="POST",
        paid=False,
    )

    result = simulate_invoke("https://api.example.com", tool)
    assert result["endpoint"] == "https://api.example.com/api/invoke"
    assert not result["endpoint"].startswith("//")
