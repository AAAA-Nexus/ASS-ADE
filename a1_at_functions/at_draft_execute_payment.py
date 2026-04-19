# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:444
# Component id: at.source.ass_ade.execute_payment
from __future__ import annotations

__version__ = "0.1.0"

def execute_payment(self, challenge: PaymentChallenge) -> PaymentResult:
    """Submit payment for the challenge.

    Returns PaymentResult with success status and details.
    Calls the lower-level submit_payment() function.
    """
    return submit_payment(challenge)
