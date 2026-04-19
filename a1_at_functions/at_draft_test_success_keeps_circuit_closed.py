# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_success_keeps_circuit_closed.py:7
# Component id: at.source.a1_at_functions.test_success_keeps_circuit_closed
from __future__ import annotations

__version__ = "0.1.0"

def test_success_keeps_circuit_closed(self) -> None:
    inner = _CountingTransport([httpx.Response(200)] * 10)
    cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
    for _ in range(5):
        resp = cb.handle_request(httpx.Request("GET", "https://example.com"))
        assert resp.status_code == 200
    assert not cb.is_open
