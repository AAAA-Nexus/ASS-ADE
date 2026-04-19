# Extracted from C:/!ass-ade/tests/test_mcp.py:131
# Component id: sy.source.ass_ade.test_mcp_invoke_redacts_sensitive_response_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_mcp_invoke_redacts_sensitive_response_fields(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(
        name="demo",
        tools=[MCPTool(name="authorize_action", endpoint="/authorize", method="POST", paid=False)],
    )
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))
    monkeypatch.setattr(
        "ass_ade.cli.invoke_tool",
        lambda *_, **__: httpx.Response(
            200,
            request=httpx.Request("POST", "https://atomadic.tech/authorize"),
            json={
                "authorized": True,
                "authorization_token": "live-token",
                "nested": {"payment_proof": "proof"},
            },
        ),
    )

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(
        app,
        ["mcp", "invoke", "authorize_action", "--config", str(config_path)],
    )

    assert result.exit_code == 0
    assert "live-token" not in result.stdout
    assert "[redacted]" in result.stdout
