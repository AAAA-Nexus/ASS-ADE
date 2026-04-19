# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1023
# Component id: mo.source.ass_ade.defi_bridge_verify
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
