# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_resilience.py:109
# Component id: at.source.ass_ade.test_success_keeps_circuit_closed
__version__ = "0.1.0"

    def test_success_keeps_circuit_closed(self) -> None:
        inner = _CountingTransport([httpx.Response(200)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
        for _ in range(5):
            resp = cb.handle_request(httpx.Request("GET", "https://example.com"))
            assert resp.status_code == 200
        assert not cb.is_open
