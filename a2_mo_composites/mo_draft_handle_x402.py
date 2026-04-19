# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:303
# Component id: mo.source.ass_ade.handle_x402
from __future__ import annotations

__version__ = "0.1.0"

def handle_x402(self, response: httpx.Response) -> dict:
    """Parse a 402 Payment Required response and return payment details.

    The x402 protocol returns payment requirements in the response body.
    This method parses the response into a dict that includes both backward-compatible
    keys and a typed PaymentChallenge for new code.

    Returns a dict with:
    - payment_required: bool (always True)
    - challenge: PaymentChallenge (typed, parsed from response)
    - amount_usdc: float (from challenge.amount_usdc)
    - network: str (blockchain network)
    - treasury: str (payment recipient)
    - endpoint: str (which endpoint requires payment)
    - detail: str (human-readable message)
    - raw: dict (original response body)
    """
    try:
        body = response.json()
    except ValueError:
        body = {}

    # Try to parse as a typed PaymentChallenge
    challenge = None
    try:
        challenge = PaymentChallenge.from_response(body)
    except ValueError:
        pass  # Fall back to loose dict format

    return {
        "payment_required": True,
        "challenge": challenge,  # New: typed PaymentChallenge
        "amount_usdc": body.get("amount") or body.get("price_usdc", 0),
        "network": body.get("network", "base"),
        "treasury": body.get("address") or body.get("treasury", ""),
        "endpoint": body.get("endpoint", ""),
        "detail": body.get("detail") or body.get("message", "Payment required"),
        "raw": body,
    }
