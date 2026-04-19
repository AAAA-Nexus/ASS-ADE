# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_retries_on_429_then_succeeds.py:7
# Component id: at.source.a1_at_functions.test_retries_on_429_then_succeeds
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
