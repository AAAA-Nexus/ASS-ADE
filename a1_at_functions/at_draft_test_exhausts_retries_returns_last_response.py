# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_exhausts_retries_returns_last_response.py:7
# Component id: at.source.a1_at_functions.test_exhausts_retries_returns_last_response
from __future__ import annotations

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
