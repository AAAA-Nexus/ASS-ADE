# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp.py:211
# Component id: sy.source.ass_ade.test_mcp_estimate_cost_free_tool
__version__ = "0.1.0"

def test_mcp_estimate_cost_free_tool(monkeypatch, tmp_path: Path) -> None:
    manifest = MCPManifest(name="demo", tools=[MCPTool(name="echo", endpoint="/echo", paid=False)])
    monkeypatch.setattr("ass_ade.cli.NexusClient", _fake_client_factory(manifest))

    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["mcp", "estimate-cost", "1", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "free" in result.stdout.lower()
