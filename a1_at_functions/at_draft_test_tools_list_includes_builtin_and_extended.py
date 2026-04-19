# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tools_list_includes_builtin_and_extended.py:7
# Component id: at.source.a1_at_functions.test_tools_list_includes_builtin_and_extended
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_list_includes_builtin_and_extended(self) -> None:
    server = MCPServer(".")
    _initialize_server(server)
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    })
    assert response is not None
    tools = response["result"]["tools"]
    names = {t["name"] for t in tools}

    # Built-in tools
    assert "read_file" in names
    assert "write_file" in names

    # Extended workflow tools
    assert "phase0_recon" in names
    assert "context_pack" in names
    assert "context_memory_store" in names
    assert "context_memory_query" in names
    assert "map_terrain" in names
    assert "trust_gate" in names
    assert "certify_output" in names
    assert "safe_execute" in names
    assert "ask_agent" in names
    assert "a2a_validate" in names
    assert "a2a_negotiate" in names
