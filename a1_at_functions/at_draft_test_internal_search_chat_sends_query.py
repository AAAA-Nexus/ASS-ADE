# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_search_x402.py:225
# Component id: at.source.ass_ade.test_internal_search_chat_sends_query
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
