# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_from_payment_result.py:7
# Component id: at.source.a1_at_functions.from_payment_result
from __future__ import annotations

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
