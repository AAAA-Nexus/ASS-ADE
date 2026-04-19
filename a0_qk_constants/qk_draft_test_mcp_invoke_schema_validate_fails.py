# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp.py:163
# Component id: qk.source.ass_ade.test_mcp_invoke_schema_validate_fails
__version__ = "0.1.0"

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
