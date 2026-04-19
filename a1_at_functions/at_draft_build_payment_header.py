# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:358
# Component id: at.source.ass_ade.build_payment_header
__version__ = "0.1.0"

def build_payment_header(result: PaymentResult) -> dict[str, str]:
    """Build the HTTP headers to submit with the paid request retry.

    Uses PaymentProof to format the PAYMENT-SIGNATURE header consistently.
    Returns empty dict if payment was unsuccessful.
    """
    proof = PaymentProof.from_payment_result(result)
    if not proof:
        return {}
    return {"PAYMENT-SIGNATURE": proof.to_header_value()}
