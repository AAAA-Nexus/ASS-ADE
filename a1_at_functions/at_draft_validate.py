# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:62
# Component id: at.source.ass_ade.validate
from __future__ import annotations

__version__ = "0.1.0"

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
