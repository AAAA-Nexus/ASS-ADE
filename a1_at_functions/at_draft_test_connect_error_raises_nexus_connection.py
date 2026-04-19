# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testretrytransport.py:50
# Component id: at.source.ass_ade.test_connect_error_raises_nexus_connection
__version__ = "0.1.0"

    def test_connect_error_raises_nexus_connection(self) -> None:
        inner = _FailingTransport(httpx.ConnectError("refused"))
        transport = RetryTransport(inner, max_retries=2, backoff_base=0.0)
        with pytest.raises(NexusConnectionError):
            transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert inner.call_count == 2
