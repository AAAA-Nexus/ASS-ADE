# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_paymentfee.py:5
# Component id: mo.source.ass_ade.paymentfee
__version__ = "0.1.0"

class PaymentFee(NexusModel):
    """/v1/payments/fee — x402 fee oracle"""
    amount: Any = None
    currency: str | None = None
    network: str | None = None
    pay_to: str | None = None
