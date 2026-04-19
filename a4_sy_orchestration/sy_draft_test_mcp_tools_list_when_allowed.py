# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_mcp_tools_list_when_allowed.py:7
# Component id: sy.source.a4_sy_orchestration.test_mcp_tools_list_when_allowed
from __future__ import annotations

__version__ = "0.1.0"

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
