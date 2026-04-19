# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_x402clientflow.py:29
# Component id: at.source.a2_mo_composites.parse_challenge
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
