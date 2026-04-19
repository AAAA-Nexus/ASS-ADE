# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_spendingbudgetresult.py:5
# Component id: mo.source.ass_ade.spendingbudgetresult
__version__ = "0.1.0"

class SpendingBudgetResult(NexusModel):
    """/v1/spending/budget — SPG-101"""
    within_budget: bool | None = None
    total_spend_usdc: float | None = None
    per_hop: list[dict] = Field(default_factory=list)
