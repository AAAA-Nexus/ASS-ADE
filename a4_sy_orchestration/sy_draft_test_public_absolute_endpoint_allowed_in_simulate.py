# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcptoolendpointssrf.py:65
# Component id: sy.source.ass_ade.test_public_absolute_endpoint_allowed_in_simulate
__version__ = "0.1.0"

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
