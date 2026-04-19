# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_ssrf_protection.py:138
# Component id: at.source.ass_ade.test_absolute_localhost_endpoint_raises
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
