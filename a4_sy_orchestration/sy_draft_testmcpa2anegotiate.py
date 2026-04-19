# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:137
# Component id: sy.source.ass_ade.testmcpa2anegotiate
__version__ = "0.1.0"

class TestMCPA2ANegotiate:
    def test_a2a_negotiate_invalid_remote(self) -> None:
        import httpx as _httpx

        server = MCPServer(".")
        _initialize_server(server)
        with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
            response = server._handle({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "a2a_negotiate", "arguments": {"remote_url": "https://bad.com"}},
            })

        assert response is not None
        assert response["result"]["isError"]
