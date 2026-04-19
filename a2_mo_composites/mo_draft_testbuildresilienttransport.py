# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testbuildresilienttransport.py:7
# Component id: mo.source.a2_mo_composites.testbuildresilienttransport
from __future__ import annotations

__version__ = "0.1.0"

class TestBuildResilientTransport:
    def test_returns_circuit_breaker_wrapping_retry(self) -> None:
        transport = build_resilient_transport(max_retries=2)
        assert isinstance(transport, CircuitBreakerTransport)
        assert isinstance(transport._wrapped, RetryTransport)
