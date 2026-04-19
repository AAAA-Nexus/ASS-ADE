# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:456
# Component id: qk.source.ass_ade.get_proof
__version__ = "0.1.0"

    def get_proof(self, payment: PaymentResult) -> PaymentProof | None:
        """Extract structured PaymentProof from a payment result."""
        return PaymentProof.from_payment_result(payment)
