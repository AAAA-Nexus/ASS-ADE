# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcptoolendpointssrf.py:7
# Component id: sy.source.a4_sy_orchestration.testmcptoolendpointssrf
from __future__ import annotations

__version__ = "0.1.0"

class TestMCPToolEndpointSSRF:
    """Test SSRF protection for MCP tool endpoint invocation."""

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

    def test_simulate_invoke_validates_absolute_endpoint(self) -> None:
        """simulate_invoke should validate absolute endpoints for SSRF."""
        from ass_ade.mcp.utils import simulate_invoke

        tool = MCPTool(
            name="bad-tool",
            endpoint="https://127.0.0.1/admin",
            method="POST",
            paid=False,
        )

        with pytest.raises(ValueError, match="blocked network address|loopback"):
            simulate_invoke("https://api.example.com", tool)

    def test_public_absolute_endpoint_allowed_in_simulate(self) -> None:
        """Public absolute endpoints should be allowed in simulate_invoke."""
        from ass_ade.mcp.utils import simulate_invoke

        tool = MCPTool(
            name="public-tool",
            endpoint="https://cloudflare.com/tool",
            method="POST",
            paid=False,
        )

        result = simulate_invoke("https://fallback.example.com", tool)
        assert result["endpoint"] == "https://cloudflare.com/tool"
