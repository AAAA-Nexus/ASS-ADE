# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:156
# Component id: mo.source.a2_mo_composites.post_with_x402
from __future__ import annotations

__version__ = "0.1.0"

def post_with_x402(self, path: str, body: dict | None = None) -> dict:
    """POST handling x402 Payment Required gracefully.

    Returns a dict with payment details instead of raising when a 402 is received.
    Includes both backward-compatible keys and a typed 'challenge' PaymentChallenge object.
    """
    return self._post_with_x402(path, body)
