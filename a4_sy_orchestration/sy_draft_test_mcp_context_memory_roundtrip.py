# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_mcp_context_memory_roundtrip.py:7
# Component id: sy.source.a4_sy_orchestration.test_mcp_context_memory_roundtrip
from __future__ import annotations

__version__ = "0.1.0"

def test_mcp_context_memory_roundtrip(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    store_response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "context_memory_store",
            "arguments": {"text": "phase zero recon context", "namespace": "demo"},
        },
    })
    query_response = server._handle({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "context_memory_query",
            "arguments": {"query": "recon", "namespace": "demo"},
        },
    })

    assert store_response is not None
    assert store_response["result"]["isError"] is False
    assert query_response is not None
    payload = json.loads(query_response["result"]["content"][0]["text"])
    assert len(payload["matches"]) == 1
