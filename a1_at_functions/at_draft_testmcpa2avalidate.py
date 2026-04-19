# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testmcpa2avalidate.py:7
# Component id: at.source.a1_at_functions.testmcpa2avalidate
from __future__ import annotations

__version__ = "0.1.0"

class TestMCPA2AValidate:
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

    def test_a2a_validate_missing_url(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "a2a_validate", "arguments": {"url": ""}},
        })
        assert response is not None
        assert response["error"]["code"] == -32602
