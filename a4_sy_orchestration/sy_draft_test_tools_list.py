# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:23
# Component id: sy.source.a4_sy_orchestration.test_tools_list
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_list(self, server: MCPServer):
    _initialize_server(server)
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    resp = server._handle(req)
    assert resp is not None
    tools = resp["result"]["tools"]
    names = {t["name"] for t in tools}
    assert "read_file" in names
    assert "write_file" in names
    assert "edit_file" in names
    assert "run_command" in names
    assert "list_directory" in names
    assert "search_files" in names
    assert "grep_search" in names
    assert "phase0_recon" in names
    assert "context_pack" in names
    assert "context_memory_store" in names
    assert "context_memory_query" in names
    assert "map_terrain" in names
    # Verify minimum expected tools; exact count may vary with additional tools
    assert len(tools) >= 19  # At least 8 builtin + 11 workflow/agent/A2A
