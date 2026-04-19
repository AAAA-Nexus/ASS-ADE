# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_resilient_transport.py:7
# Component id: at.source.a1_at_functions.build_resilient_transport
from __future__ import annotations

__version__ = "0.1.0"

def build_resilient_transport(
    *,
    max_retries: int = 3,
    backoff_base: float = 0.5,
    circuit_failure_threshold: int = 5,
    circuit_window_s: float = 60.0,
    circuit_recovery_s: float = 30.0,
    cancellation_context: CancellationContext | None = None,
) -> httpx.BaseTransport:
    """Build a composed transport stack: CircuitBreaker (outer) → Retry (middle) → HTTP (inner).

    Requests traverse: CircuitBreaker → Retry → HTTP.

    Args:
        cancellation_context: Optional context for cooperative cancellation support.
            If provided, the retry transport will check for cancellation between
            retry attempts and abort with NexusConnectionError if cancelled.
    """
    base = httpx.HTTPTransport()
    retrying = RetryTransport(
        base,
        max_retries=max_retries,
        backoff_base=backoff_base,
        cancellation_context=cancellation_context,
    )
    return CircuitBreakerTransport(
        retrying,
        failure_threshold=circuit_failure_threshold,
        window_s=circuit_window_s,
        recovery_s=circuit_recovery_s,
    )
