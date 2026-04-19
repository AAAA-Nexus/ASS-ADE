# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testretrytransport.py:13
# Component id: at.source.ass_ade.test_retries_on_500_then_succeeds
__version__ = "0.1.0"

    def test_retries_on_500_then_succeeds(self) -> None:
        inner = _CountingTransport([
            httpx.Response(500),
            httpx.Response(200),
        ])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 200
        assert inner.call_count == 2
