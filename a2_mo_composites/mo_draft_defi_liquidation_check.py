# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1013
# Component id: mo.source.ass_ade.defi_liquidation_check
__version__ = "0.1.0"

    def defi_liquidation_check(self, position: dict | None = None, **kwargs: Any) -> LiquidationCheck:
        """/v1/defi/liquidation-check — health factor + time-to-liquidation (LQS-100). $0.04 + 1% equity"""
        resolved_position = position or {
            "position_id": kwargs.pop("position_id", None),
            "collateral_value": kwargs.pop("collateral_value", None),
            "debt_value": kwargs.pop("debt_value", None),
            "collateral_factor": kwargs.pop("collateral_factor", None),
        }
        return self._post_model("/v1/defi/liquidation-check", LiquidationCheck, {"position": resolved_position, **kwargs})
