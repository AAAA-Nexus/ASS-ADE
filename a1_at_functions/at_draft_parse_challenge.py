# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:392
# Component id: at.source.ass_ade.parse_challenge
from __future__ import annotations

__version__ = "0.1.0"

def parse_challenge(self, response_dict: dict) -> PaymentChallenge | None:
    """Parse a 402 response dict into a PaymentChallenge.

    Returns None if parsing fails; check last_error for details.
    """
    try:
        return PaymentChallenge.from_response(response_dict)
    except ValueError as e:
        self.last_error = str(e)
        return None
