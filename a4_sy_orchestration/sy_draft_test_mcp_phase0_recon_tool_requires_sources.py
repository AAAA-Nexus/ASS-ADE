# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_recon_context.py:109
# Component id: sy.source.ass_ade.test_mcp_phase0_recon_tool_requires_sources
__version__ = "0.1.0"

def test_mcp_phase0_recon_tool_requires_sources(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    server = MCPServer(str(tmp_path))
    _initialize_server(server)

    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "phase0_recon",
            "arguments": {"task_description": "Add an MCP tool schema"},
        },
    })

    assert response is not None
    assert response["result"]["isError"] is True
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["verdict"] == "RECON_REQUIRED"
