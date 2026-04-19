# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:186
# Component id: mo.source.ass_ade.test_get_nexus_client_uses_configured_api_key
from __future__ import annotations

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
