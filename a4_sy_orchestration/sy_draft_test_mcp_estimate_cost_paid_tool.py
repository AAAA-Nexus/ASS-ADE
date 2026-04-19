# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp.py:223
# Component id: sy.source.ass_ade.test_mcp_estimate_cost_paid_tool
__version__ = "0.1.0"

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
