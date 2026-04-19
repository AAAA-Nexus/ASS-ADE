# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_resilience.py:108
# Component id: mo.source.ass_ade.testcircuitbreakertransport
__version__ = "0.1.0"

class TestCircuitBreakerTransport:
    def test_success_keeps_circuit_closed(self) -> None:
        inner = _CountingTransport([httpx.Response(200)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
        for _ in range(5):
            resp = cb.handle_request(httpx.Request("GET", "https://example.com"))
            assert resp.status_code == 200
        assert not cb.is_open

    def test_consecutive_5xx_trips_circuit(self) -> None:
        inner = _CountingTransport([httpx.Response(500)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=30)
        for _ in range(3):
            cb.handle_request(httpx.Request("GET", "https://example.com"))
        assert cb.is_open

    def test_open_circuit_raises_immediately(self) -> None:
        inner = _CountingTransport([httpx.Response(500)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=2, window_s=60, recovery_s=30)
        for _ in range(2):
            cb.handle_request(httpx.Request("GET", "https://example.com"))
        with pytest.raises(NexusCircuitOpen):
            cb.handle_request(httpx.Request("GET", "https://example.com"))

    def test_success_after_failures_resets(self) -> None:
        responses = [httpx.Response(500), httpx.Response(200)]
        inner = _CountingTransport(responses)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
        cb.handle_request(httpx.Request("GET", "https://example.com"))  # 500
        cb.handle_request(httpx.Request("GET", "https://example.com"))  # 200 resets
        assert not cb.is_open
