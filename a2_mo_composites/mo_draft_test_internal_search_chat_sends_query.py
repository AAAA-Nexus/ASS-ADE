# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testnexusclientsearch.py:23
# Component id: mo.source.a2_mo_composites.test_internal_search_chat_sends_query
from __future__ import annotations

__version__ = "0.1.0"

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
