# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_test_mcp_invoke_paid_requires_confirm.py:5
# Component id: sy.source.ass_ade.test_mcp_invoke_paid_requires_confirm
__version__ = "0.1.0"

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
