# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:101
# Component id: at.source.ass_ade.test_a2a_validate_success
from __future__ import annotations

__version__ = "0.1.0"

def test_a2a_validate_success(self) -> None:
    card_data = {"name": "Test", "description": "d", "url": "https://test.com", "version": "1.0"}
    mock_response = MagicMock()
    mock_response.json.return_value = card_data

    server = MCPServer(".")
    _initialize_server(server)
    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO), \
         patch("ass_ade.a2a.httpx.get", return_value=mock_response):
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "a2a_validate", "arguments": {"url": "https://test.com"}},
        })

    assert response is not None
    result_data = json.loads(response["result"]["content"][0]["text"])
    assert result_data["valid"] is True
