# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_write_file_is_destructive.py:7
# Component id: at.source.a1_at_functions.test_write_file_is_destructive
from __future__ import annotations

__version__ = "0.1.0"

def test_write_file_is_destructive(self) -> None:
    server = MCPServer(".")
    _initialize_server(server)
    response = server._handle({
        "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
    })
    tools = {t["name"]: t for t in response["result"]["tools"]}
    assert tools["write_file"]["annotations"]["destructiveHint"] is True
    assert tools["write_file"]["annotations"]["readOnlyHint"] is False
