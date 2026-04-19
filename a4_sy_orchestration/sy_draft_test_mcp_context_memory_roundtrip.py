# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_recon_context.py:130
# Component id: sy.source.ass_ade.test_mcp_context_memory_roundtrip
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
