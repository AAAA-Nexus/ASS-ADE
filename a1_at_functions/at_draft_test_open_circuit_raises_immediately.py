# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_open_circuit_raises_immediately.py:7
# Component id: at.source.a1_at_functions.test_open_circuit_raises_immediately
from __future__ import annotations

__version__ = "0.1.0"

def test_open_circuit_raises_immediately(self) -> None:
    inner = _CountingTransport([httpx.Response(500)] * 10)
    cb = CircuitBreakerTransport(inner, failure_threshold=2, window_s=60, recovery_s=30)
    for _ in range(2):
        cb.handle_request(httpx.Request("GET", "https://example.com"))
    with pytest.raises(NexusCircuitOpen):
        cb.handle_request(httpx.Request("GET", "https://example.com"))
