# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_spendingauthresult.py:5
# Component id: mo.source.ass_ade.spendingauthresult
__version__ = "0.1.0"

class SpendingAuthResult(NexusModel):
    """/v1/spending/authorize — SPG-100"""
    approved: bool | None = None
    approved_amount_usdc: float | None = None
    tau_trust_decay: float | None = None
