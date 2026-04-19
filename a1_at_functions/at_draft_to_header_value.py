# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:156
# Component id: at.source.ass_ade.to_header_value
__version__ = "0.1.0"

    def to_header_value(self) -> str:
        """Format as HTTP header value (PAYMENT-SIGNATURE)."""
        return f"{self.signature};{self.wallet_address};{self.transaction_id};{self.amount_micro_usdc}"
