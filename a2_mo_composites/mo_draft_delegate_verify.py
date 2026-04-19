# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:496
# Component id: mo.source.ass_ade.delegate_verify
from __future__ import annotations

__version__ = "0.1.0"

def delegate_verify(
    self,
    chain: list[dict] | None = None,
    *,
    token: str | None = None,
    **kwargs: Any,
) -> DelegationValidation:
    """/v1/delegate/verify — full UCAN chain validation (D_MAX=23). $0.080/call"""
    if chain is None:
        chain = [{"token": token}] if token is not None else []
    return self._post_model("/v1/delegate/verify", DelegationValidation, {"chain": chain, **kwargs})
