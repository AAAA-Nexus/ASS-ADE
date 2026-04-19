# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:91
# Component id: sy.source.a4_sy_orchestration.test_tools_call_write_file
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_call_write_file(self, server: MCPServer, tmp_path: Path):
    _initialize_server(server)
    req = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {"path": "new.py", "content": "x = 1\n"},
        },
    }
    resp = server._handle(req)
    assert resp["result"]["isError"] is False
    assert (tmp_path / "new.py").read_text() == "x = 1\n"
