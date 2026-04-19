# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentchallenge.py:7
# Component id: mo.source.a2_mo_composites.paymentchallenge
from __future__ import annotations

__version__ = "0.1.0"

class PaymentChallenge:
    """Parsed x402 payment challenge from a 402 response."""
    amount_micro_usdc: int
    amount_usdc: float
    recipient: str
    nonce: str
    expires: int
    chain_id: int
    token_address: str
    endpoint: str
    x402_version: str = "2.1"

    def validate(self) -> PaymentChallenge:
        """Validate the challenge before any user consent or payment attempt."""
        if self.amount_micro_usdc <= 0:
            raise ValueError("402 response missing required field: amount_micro_usdc")
        if self.amount_micro_usdc > MAX_CHALLENGE_MICRO_USDC:
            raise ValueError(
                f"402 response amount {self.amount_micro_usdc} outside valid range "
                f"(1-{MAX_CHALLENGE_MICRO_USDC})"
            )
        if not self.recipient.strip():
            raise ValueError("402 response missing required field: recipient")
        if self.recipient.strip().lower() != ATOMADIC_TREASURY.lower():
            raise ValueError("402 response recipient does not match expected treasury")
        return self

    @classmethod
    def from_response(cls, body: dict) -> PaymentChallenge:
        """Parse a 402 JSON response body into a PaymentChallenge."""
        recipient = body.get("recipient", "")
        amount_raw = body.get("amount_micro_usdc", 0)
        if not recipient:
            raise ValueError("402 response missing required field: recipient")
        try:
            amount = int(amount_raw)
        except (TypeError, ValueError):
            raise ValueError("402 response field amount_micro_usdc must be an integer") from None
        challenge = cls(
            amount_micro_usdc=amount,
            amount_usdc=float(body.get("amount_usdc", 0)),
            recipient=recipient,
            nonce=body.get("nonce", ""),
            expires=body.get("expires", 0),
            chain_id=body.get("chain_id", BASE_MAINNET_CHAIN_ID),
            token_address=body.get("token_address") or body.get("sdk_hints", {}).get("token_address", ""),
            endpoint=body.get("endpoint", ""),
            x402_version=body.get("x402_version", "2.1"),
        )
        return challenge.validate()

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires if self.expires else False

    @property
    def display_amount(self) -> str:
        if self.amount_usdc:
            return f"${self.amount_usdc:.6f} USDC"
        return f"{self.amount_micro_usdc} micro-USDC"
