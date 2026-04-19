# Extracted from C:/!ass-ade/tests/test_resilience.py:73
# Component id: at.source.ass_ade.test_exhausts_retries_returns_last_response
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
