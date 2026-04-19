# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:363
# Component id: qk.source.ass_ade.test_progress_token_extracted_from_meta
from __future__ import annotations

__version__ = "0.1.0"

def test_progress_token_extracted_from_meta(self, tmp_path) -> None:
    """_meta.progressToken is accepted in tools/call params without error."""
    # Create the server rooted at tmp_path so the file is within working dir.
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    # read_file is a builtin tool; it runs synchronously without progress,
    # but the server must accept the _meta field without error.
    test_file = tmp_path / "meta_test.txt"
    test_file.write_text("hello")
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {"path": "meta_test.txt"},
            "_meta": {"progressToken": "tok-1"},
        },
    })
    assert response is not None
    assert response["result"]["isError"] is False
