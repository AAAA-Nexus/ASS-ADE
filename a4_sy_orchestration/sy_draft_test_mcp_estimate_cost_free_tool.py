# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_mcp_estimate_cost_free_tool.py:7
# Component id: sy.source.a4_sy_orchestration.test_mcp_estimate_cost_free_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_mcp_estimate_cost_free_tool(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", paid=False)])
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "estimate-cost", "1", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "free" in result.stdout.lower()
