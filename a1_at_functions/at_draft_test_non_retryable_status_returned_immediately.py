# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testretrytransport.py:57
# Component id: at.source.ass_ade.test_non_retryable_status_returned_immediately
__version__ = "0.1.0"

    def test_non_retryable_status_returned_immediately(self) -> None:
        inner = _CountingTransport([httpx.Response(404)])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 404
        assert inner.call_count == 1
