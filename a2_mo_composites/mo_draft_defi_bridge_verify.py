# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:828
# Component id: mo.source.a2_mo_composites.defi_bridge_verify
from __future__ import annotations

__version__ = "0.1.0"

def defi_bridge_verify(
    self,
    bridge: str | None = None,
    amount_usdc: float = 0.0,
    *,
    bridge_id: str | None = None,
    **kwargs: Any,
) -> BridgeVerify:
    """/v1/defi/bridge-verify — cross-chain bridge integrity (BRP-100). $0.08/verification"""
    return self._post_model("/v1/defi/bridge-verify", BridgeVerify, {"bridge": bridge or bridge_id or "", "amount_usdc": amount_usdc, **kwargs})
