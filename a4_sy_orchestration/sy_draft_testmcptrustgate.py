# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:158
# Component id: sy.source.ass_ade.testmcptrustgate
__version__ = "0.1.0"

class TestMCPTrustGate:
    def test_trust_gate_requires_agent_id(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "trust_gate", "arguments": {"agent_id": ""}},
        })
        assert response is not None
        assert response["error"]["code"] == -32602

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

    def test_get_nexus_client_uses_configured_api_key(self) -> None:
        server = MCPServer(".")
        cfg = AssAdeConfig(
            profile="hybrid",
            nexus_base_url="https://atomadic.tech",
            request_timeout_s=12.0,
            nexus_api_key="test-secret",
        )

        with (
            patch("ass_ade.config.load_config", return_value=cfg),
            patch("ass_ade.nexus.client.NexusClient") as client_cls,
        ):
            client = server._get_nexus_client()

        assert client is client_cls.return_value
        client_cls.assert_called_once_with(
            base_url="https://atomadic.tech",
            timeout=12.0,
            api_key="test-secret",
        )
