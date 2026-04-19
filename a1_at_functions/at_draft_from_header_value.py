# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:161
# Component id: at.source.ass_ade.from_header_value
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
