# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_resilient.py:7
# Component id: at.source.a1_at_functions.resilient
from __future__ import annotations

__version__ = "0.1.0"

def resilient(
    cls,
    *,
    base_url: str,
    timeout: float = 20.0,
    api_key: str | None = None,
    max_retries: int = 3,
    circuit_failure_threshold: int = 5,
) -> NexusClient:
    """Create a client pre-configured with retry + circuit-breaker transports."""
    from ass_ade.nexus.resilience import build_resilient_transport

    transport = build_resilient_transport(
        max_retries=max_retries,
        circuit_failure_threshold=circuit_failure_threshold,
    )
    return cls(base_url=base_url, timeout=timeout, transport=transport, api_key=api_key)
