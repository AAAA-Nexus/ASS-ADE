# Extracted from C:/!ass-ade/tests/test_resilience.py:117
# Component id: at.source.ass_ade.test_consecutive_5xx_trips_circuit
from __future__ import annotations

__version__ = "0.1.0"

def test_consecutive_5xx_trips_circuit(self) -> None:
    inner = _CountingTransport([httpx.Response(500)] * 10)
    cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=30)
    for _ in range(3):
        cb.handle_request(httpx.Request("GET", "https://example.com"))
    assert cb.is_open
