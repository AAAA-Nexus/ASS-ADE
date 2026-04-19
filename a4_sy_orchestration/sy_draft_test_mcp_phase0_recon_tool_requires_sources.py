# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_mcp_phase0_recon_tool_requires_sources.py:7
# Component id: sy.source.a4_sy_orchestration.test_mcp_phase0_recon_tool_requires_sources
from __future__ import annotations

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
