# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:291
# Component id: sy.source.ass_ade.test_read_file_is_readonly
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
