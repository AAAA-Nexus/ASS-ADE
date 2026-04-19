# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_returns_circuit_breaker_wrapping_retry.py:7
# Component id: at.source.a1_at_functions.test_returns_circuit_breaker_wrapping_retry
from __future__ import annotations

__version__ = "0.1.0"

def test_returns_circuit_breaker_wrapping_retry(self) -> None:
    transport = build_resilient_transport(max_retries=2)
    assert isinstance(transport, CircuitBreakerTransport)
    assert isinstance(transport._wrapped, RetryTransport)
