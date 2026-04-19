# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_paymentproof.py:20
# Component id: qk.source.ass_ade.from_payment_result
__version__ = "0.1.0"

    def from_payment_result(cls, result: PaymentResult) -> PaymentProof | None:
        """Parse a PaymentProof from a successful PaymentResult."""
        if not result.success or not result.signature_header:
            return None
        try:
            parts = result.signature_header.split(";")
            if len(parts) != 4:
                return None
            sig, addr, txid, amount_str = parts
            return cls(
                signature=sig,
                wallet_address=addr,
                transaction_id=txid,
                amount_micro_usdc=int(amount_str),
            )
        except (ValueError, IndexError):
            return None
