# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testmcp202511features.py:53
# Component id: og.source.a3_og_features.test_run_command_is_open_world
from __future__ import annotations

__version__ = "0.1.0"

def test_run_command_is_open_world(self) -> None:
    server = MCPServer(".")
    _initialize_server(server)
    response = server._handle({
        "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
    })
    tools = {t["name"]: t for t in response["result"]["tools"]}
    assert tools["run_command"]["annotations"]["openWorldHint"] is True
