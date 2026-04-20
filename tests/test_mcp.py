from pathlib import Path

import httpx
from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig, write_default_config
from ass_ade.mcp.utils import invoke_tool
from ass_ade.nexus.models import MCPManifest, MCPTool

runner = CliRunner()


def test_mcp_tools_require_remote_opt_in_for_local_profile(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["mcp", "tools", "--config", str(config_path)])

    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout


def test_mcp_tools_list_when_allowed(monkeypatch, tmp_path: Path) -> None:
    # Fake manifest returned by NexusClient
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", method="POST", paid=False)])

    class FakeClient:
        def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get_mcp_manifest(self):
            return manifest

    monkeypatch.setattr("ass_ade.cli.NexusClient", FakeClient)

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "tools", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "MCP Tools" in result.stdout
    assert "echo" in result.stdout


def test_mcp_invoke_paid_requires_confirm(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="paid-tool", endpoint="/pay", method="POST", paid=True)])

    class FakeClient:
        def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get_mcp_manifest(self):
            return manifest

    monkeypatch.setattr("ass_ade.cli.NexusClient", FakeClient)

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "invoke", "1", "--config", str(config_path)])

    assert result.exit_code == 3
    assert "paid" in result.stdout.lower()


def test_mcp_invoke_dry_run(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", method="POST", paid=False)])

    class FakeClient:
        def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get_mcp_manifest(self):
            return manifest

    monkeypatch.setattr("ass_ade.cli.NexusClient", FakeClient)

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "invoke", "1", "--config", str(config_path), "--dry-run"]) 

    assert result.exit_code == 0
    assert '"simulated"' in result.stdout.lower()


def test_invoke_tool_forwards_api_key() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("Authorization", "")
        captured["x_api_key"] = request.headers.get("X-API-Key", "")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    tool = MCPTool(name="paid-tool", endpoint="/paid", method="POST", paid=True)

    response = invoke_tool(
        "https://atomadic.tech",
        tool,
        {"probe": True},
        api_key="test-secret",
        transport=transport,
    )

    assert response.status_code == 200
    assert captured["authorization"] == "Bearer test-secret"
    assert captured["x_api_key"] == "test-secret"


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


def test_mcp_invoke_schema_validate_fails(monkeypatch, tmp_path: Path) -> None:
    # Tool schema requires property 'name' (string)
    schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", method="POST", paid=False, inputSchema=schema)])

    class FakeClient:
        def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get_mcp_manifest(self):
            return manifest

    monkeypatch.setattr("ass_ade.cli.NexusClient", FakeClient)

    # write a payload that misses the required 'name'
    payload_file = tmp_path / "payload.json"
    payload_file.write_text("{}", encoding="utf-8")

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(
        app,
        ["mcp", "invoke", "1", "--config", str(config_path), "--input-file", str(payload_file), "--dry-run", "--schema-validate"],
    )

    assert result.exit_code != 0
    assert "schema validation failed" in result.stdout.lower()


# ── estimate-cost tests ────────────────────────────────────────────────────────

def _fake_client_factory(manifest):
    class FakeClient:
        def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
            pass
        def __enter__(self): return self
        def __exit__(self, *_): return False
        def get_mcp_manifest(self): return manifest
    return FakeClient


def test_mcp_estimate_cost_free_tool(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", paid=False)])
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "estimate-cost", "1", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "free" in result.stdout.lower()


def test_mcp_estimate_cost_paid_tool(monkeypatch, tmp_path: Path) -> None:
    from ass_ade.nexus.models import CostEstimate
    tool = MCPTool(name="premium", endpoint="/premium", paid=True, cost=CostEstimate(unit_cost=0.01, currency="USDC"))
    manifest = MCPManifest(name="demo", tools=[tool])
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "estimate-cost", "1", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "0.01" in result.stdout


# ── dry-run --json-out test ────────────────────────────────────────────────────

def test_mcp_invoke_dry_run_json_out(monkeypatch, tmp_path: Path) -> None:
    import json as _json
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", method="POST", paid=False)])
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)
    out_file = tmp_path / "sim.json"

    result = runner.invoke(
        app,
        ["mcp", "invoke", "1", "--config", str(config_path), "--dry-run", "--json-out", str(out_file)],
    )
    assert result.exit_code == 0
    assert out_file.exists()
    payload = _json.loads(out_file.read_text(encoding="utf-8"))
    assert payload.get("simulated") is True


# ── mock server test ───────────────────────────────────────────────────────────

def test_mock_server_serves_manifest() -> None:
    import httpx

    from ass_ade.mcp.mock_server import start_server

    server = start_server(port=19787, block=False)
    try:
        resp = httpx.get("http://127.0.0.1:19787/.well-known/mcp.json", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert "tools" in data
    finally:
        server.shutdown()


def test_mock_server_oversized_body_returns_413_with_content_length() -> None:
    import httpx

    from ass_ade.mcp.mock_server import _MAX_BODY_BYTES, start_server

    server = start_server(port=19788, block=False)
    try:
        payload = b"x" * (_MAX_BODY_BYTES + 1)
        resp = httpx.post(
            "http://127.0.0.1:19788/tools/echo",
            content=payload,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert resp.status_code == 413
        assert "Content-Length" in resp.headers
        assert int(resp.headers["Content-Length"]) == len(resp.content)
        assert resp.json()["error"] == "request entity too large"
    finally:
        server.shutdown()

