# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:138
# Component id: at.source.ass_ade.from_payment_result
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
