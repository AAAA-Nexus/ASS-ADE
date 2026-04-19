# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testretrytransport.py:32
# Component id: at.source.ass_ade.test_exhausts_retries_returns_last_response
__version__ = "0.1.0"

    def test_exhausts_retries_returns_last_response(self) -> None:
        inner = _CountingTransport([
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(503),
        ])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 503
        assert inner.call_count == 3
