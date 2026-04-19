# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_connect_error_raises_nexus_connection.py:7
# Component id: at.source.a1_at_functions.test_connect_error_raises_nexus_connection
from __future__ import annotations

__version__ = "0.1.0"

def test_connect_error_raises_nexus_connection(self) -> None:
    inner = _FailingTransport(httpx.ConnectError("refused"))
    transport = RetryTransport(inner, max_retries=2, backoff_base=0.0)
    with pytest.raises(NexusConnectionError):
        transport.handle_request(httpx.Request("GET", "https://example.com"))
    assert inner.call_count == 2
