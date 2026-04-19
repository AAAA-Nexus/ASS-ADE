# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_resilience.py:144
# Component id: at.source.ass_ade.test_returns_circuit_breaker_wrapping_retry
__version__ = "0.1.0"

    def test_returns_circuit_breaker_wrapping_retry(self) -> None:
        transport = build_resilient_transport(max_retries=2)
        assert isinstance(transport, CircuitBreakerTransport)
        assert isinstance(transport._wrapped, RetryTransport)
