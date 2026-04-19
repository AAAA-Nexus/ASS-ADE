# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:123
# Component id: qk.source.ass_ade.paymentproof
from __future__ import annotations

__version__ = "0.1.0"

class PaymentProof:
    """Structured proof of x402 payment for request retry.

    The payment proof is encoded as an HTTP header: PAYMENT-SIGNATURE
    Format: <signature_hex>;<wallet_address>;<transaction_id>;<amount_micro_usdc>

    This structure formalizes the contract between client (who creates it)
    and server (who validates it).
    """
    signature: str  # hex-encoded transaction signature
    wallet_address: str  # sender's wallet address (checksummed)
    transaction_id: str  # blockchain transaction ID
    amount_micro_usdc: int  # USDC amount in micro units

    @classmethod
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

    def to_header_value(self) -> str:
        """Format as HTTP header value (PAYMENT-SIGNATURE)."""
        return f"{self.signature};{self.wallet_address};{self.transaction_id};{self.amount_micro_usdc}"

    @classmethod
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
