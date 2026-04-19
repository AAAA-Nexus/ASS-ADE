# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_mcp_invoke_dry_run_json_out.py:7
# Component id: sy.source.a4_sy_orchestration.test_mcp_invoke_dry_run_json_out
from __future__ import annotations

__version__ = "0.1.0"

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
