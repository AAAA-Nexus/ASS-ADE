# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:39
# Component id: sy.source.ass_ade.server
__version__ = "0.1.0"

    def server(self, tmp_path: Path) -> MCPServer:
        (tmp_path / "hello.py").write_text("print('hi')\n")
        return MCPServer(working_dir=str(tmp_path))
