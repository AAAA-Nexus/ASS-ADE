# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/mock_server.py:51
# Component id: sy.source.ass_ade.do_get
__version__ = "0.1.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/.well-known/mcp.json", "/mcp.json"):
            self._send_json(200, self.manifest)
        elif self.path == "/health":
            self._send_json(200, {"status": "ok", "version": "mock"})
        else:
            self._send_json(404, {"error": "not found"})
