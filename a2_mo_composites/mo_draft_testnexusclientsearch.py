# Extracted from C:/!ass-ade/tests/test_search_x402.py:209
# Component id: mo.source.ass_ade.testnexusclientsearch
from __future__ import annotations

__version__ = "0.1.0"

class TestNexusClientSearch:
    def test_internal_search_sends_session_token(self) -> None:
        """internal_search should include X-Owner-Token header."""
        requests_made = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests_made.append(request)
            return httpx.Response(200, json={"success": True, "result": {}})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        client.internal_search("test query", session_token="my-session-123")
        assert len(requests_made) == 1
        assert requests_made[0].headers.get("X-Owner-Token") == "my-session-123"
        client.close()

    def test_internal_search_chat_sends_query(self) -> None:
        """internal_search_chat should POST to /internal/search/chat."""
        requests_made = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests_made.append(request)
            return httpx.Response(200, json={"success": True, "result": {"response": "answer"}})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client.internal_search_chat("what is codex", session_token="sess")
        assert result["success"] is True
        assert "/internal/search/chat" in str(requests_made[0].url)
        client.close()
