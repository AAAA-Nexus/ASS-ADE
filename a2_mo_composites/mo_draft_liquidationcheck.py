# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_liquidationcheck.py:5
# Component id: mo.source.ass_ade.liquidationcheck
__version__ = "0.1.0"

class LiquidationCheck(NexusModel):
    """/v1/defi/liquidation-check — LQS-100"""
    health_factor: float | None = None
    time_to_liquidation_s: int | None = None
    recommended_top_up_usdc: float | None = None
