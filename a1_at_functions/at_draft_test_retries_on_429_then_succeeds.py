# Extracted from C:/!ass-ade/tests/test_resilience.py:64
# Component id: at.source.ass_ade.test_retries_on_429_then_succeeds
from __future__ import annotations

__version__ = "0.1.0"

def test_retries_on_429_then_succeeds(self) -> None:
    inner = _CountingTransport([
        httpx.Response(429, headers={"retry-after": "0"}),
        httpx.Response(200),
    ])
    transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
    response = transport.handle_request(httpx.Request("GET", "https://example.com"))
    assert response.status_code == 200
