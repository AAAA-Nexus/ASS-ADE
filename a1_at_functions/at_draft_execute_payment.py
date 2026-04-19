# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_execute_payment.py:7
# Component id: at.source.a1_at_functions.execute_payment
from __future__ import annotations

__version__ = "0.1.0"

def execute_payment(self, challenge: PaymentChallenge) -> PaymentResult:
    """Submit payment for the challenge.

    Returns PaymentResult with success status and details.
    Calls the lower-level submit_payment() function.
    """
    return submit_payment(challenge)
