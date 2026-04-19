# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testmcp202511features.py:33
# Component id: og.source.a3_og_features.test_read_file_is_readonly
from __future__ import annotations

__version__ = "0.1.0"

def test_read_file_is_readonly(self) -> None:
    server = MCPServer(".")
    _initialize_server(server)
    response = server._handle({
        "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
    })
    tools = {t["name"]: t for t in response["result"]["tools"]}
    assert tools["read_file"]["annotations"]["readOnlyHint"] is True
    assert tools["read_file"]["annotations"]["destructiveHint"] is False
