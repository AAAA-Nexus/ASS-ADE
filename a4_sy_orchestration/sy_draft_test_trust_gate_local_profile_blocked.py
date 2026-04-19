# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:171
# Component id: sy.source.ass_ade.test_trust_gate_local_profile_blocked
__version__ = "0.1.0"

    def test_trust_gate_local_profile_blocked(self) -> None:

        server = MCPServer(".")
        _initialize_server(server)
        # Mock load_config to return local profile
        with patch("ass_ade.mcp.server.MCPServer._get_nexus_client", side_effect=RuntimeError("local")):
            response = server._handle({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "trust_gate", "arguments": {"agent_id": "test-agent"}},
            })
        assert response is not None
        assert response["result"]["isError"]
