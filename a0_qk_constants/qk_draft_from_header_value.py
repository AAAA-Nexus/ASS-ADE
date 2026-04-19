# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_paymentproof.py:43
# Component id: qk.source.ass_ade.from_header_value
__version__ = "0.1.0"

    def from_header_value(cls, header_value: str) -> PaymentProof | None:
        """Parse from HTTP header value (PAYMENT-SIGNATURE)."""
        try:
            parts = header_value.split(";")
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
