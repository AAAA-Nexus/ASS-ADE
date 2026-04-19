# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentchallenge.py:35
# Component id: at.source.a2_mo_composites.from_response
from __future__ import annotations

__version__ = "0.1.0"

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
