# Extracted from C:/!ass-ade/tests/test_map_terrain.py:229
# Component id: sy.source.ass_ade.test_mcp_map_terrain_tool_halts_for_missing_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_mcp_map_terrain_tool_halts_for_missing_tool(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    response = server._handle(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "map_terrain",
                "arguments": {
                    "task_description": "Need a missing scanner.",
                    "required_capabilities": {"tools": ["nexus_semgrep_scan"]},
                },
            },
        }
    )

    assert response is not None
    assert response["result"]["isError"] is True
    text = response["result"]["content"][0]["text"]
    assert '"verdict": "HALT_AND_INVENT"' in text
