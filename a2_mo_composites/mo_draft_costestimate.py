# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_costestimate.py:5
# Component id: mo.source.ass_ade.costestimate
__version__ = "0.1.0"

class CostEstimate(NexusModel):
    currency: str = "USDC"
    unit_cost: float | None = None
    rate_limit_rpm: int | None = None
    rate_limit_tpm: int | None = None
    notes: str | None = None
