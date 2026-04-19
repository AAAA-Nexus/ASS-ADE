# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:976
# Component id: mo.source.ass_ade.defi_optimize
__version__ = "0.1.0"

    def defi_optimize(
        self,
        protocol: str | None = None,
        position_size_usdc: float | None = None,
        *,
        payload: dict | None = None,
        **kwargs: Any,
    ) -> DefiOptimize:
        """/v1/defi/optimize — optimal LP parameters (DFP-100). $0.08 + 0.2% of position"""
        if payload is not None:
            protocol = protocol or payload.get("protocol") or payload.get("pool") or payload.get("market")
            position_size_usdc = (
                position_size_usdc
                if position_size_usdc is not None
                else payload.get("position_size_usdc")
                or payload.get("amount_usdc")
                or payload.get("capital_usdc")
            )
        return self._post_model("/v1/defi/optimize", DefiOptimize, {
            "protocol": protocol or "", "position_size_usdc": position_size_usdc or 0.0, **kwargs,
        })
