# Extracted from C:/!ass-ade/tests/test_resilience.py:132
# Component id: at.source.ass_ade.test_success_after_failures_resets
from __future__ import annotations

__version__ = "0.1.0"

def test_success_after_failures_resets(self) -> None:
    responses = [httpx.Response(500), httpx.Response(200)]
    inner = _CountingTransport(responses)
    cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
    cb.handle_request(httpx.Request("GET", "https://example.com"))  # 500
    cb.handle_request(httpx.Request("GET", "https://example.com"))  # 200 resets
    assert not cb.is_open
