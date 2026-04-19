# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_paymentproof.py:38
# Component id: qk.source.ass_ade.to_header_value
__version__ = "0.1.0"

    def to_header_value(self) -> str:
        """Format as HTTP header value (PAYMENT-SIGNATURE)."""
        return f"{self.signature};{self.wallet_address};{self.transaction_id};{self.amount_micro_usdc}"
