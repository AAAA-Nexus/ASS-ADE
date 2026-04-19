# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_paymentproof.py:40
# Component id: qk.source.a0_qk_constants.to_header_value
from __future__ import annotations

__version__ = "0.1.0"

def to_header_value(self) -> str:
    """Format as HTTP header value (PAYMENT-SIGNATURE)."""
    return f"{self.signature};{self.wallet_address};{self.transaction_id};{self.amount_micro_usdc}"
