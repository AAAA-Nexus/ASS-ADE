# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcptrustgate.py:33
# Component id: mo.source.ass_ade.test_get_nexus_client_uses_configured_api_key
__version__ = "0.1.0"

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
