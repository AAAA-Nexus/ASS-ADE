# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_post_with_x402.py:7
# Component id: at.source.a1_at_functions.post_with_x402
from __future__ import annotations

__version__ = "0.1.0"

def post_with_x402(self, path: str, body: dict | None = None) -> dict:
    """POST handling x402 Payment Required gracefully.

    Returns a dict with payment details instead of raising when a 402 is received.
    Includes both backward-compatible keys and a typed 'challenge' PaymentChallenge object.
    """
    return self._post_with_x402(path, body)
