# Extracted from C:/!ass-ade/tests/test_resilience.py:124
# Component id: at.source.ass_ade.test_open_circuit_raises_immediately
from __future__ import annotations

__version__ = "0.1.0"

def test_open_circuit_raises_immediately(self) -> None:
    inner = _CountingTransport([httpx.Response(500)] * 10)
    cb = CircuitBreakerTransport(inner, failure_threshold=2, window_s=60, recovery_s=30)
    for _ in range(2):
        cb.handle_request(httpx.Request("GET", "https://example.com"))
    with pytest.raises(NexusCircuitOpen):
        cb.handle_request(httpx.Request("GET", "https://example.com"))
