# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_resilience.py:143
# Component id: mo.source.ass_ade.testbuildresilienttransport
__version__ = "0.1.0"

class TestBuildResilientTransport:
    def test_returns_circuit_breaker_wrapping_retry(self) -> None:
        transport = build_resilient_transport(max_retries=2)
        assert isinstance(transport, CircuitBreakerTransport)
        assert isinstance(transport._wrapped, RetryTransport)
