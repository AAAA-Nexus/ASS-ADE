# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_can_pay_expired.py:7
# Component id: at.source.a1_at_functions.test_can_pay_expired
from __future__ import annotations

__version__ = "0.1.0"

def test_can_pay_expired(self) -> None:
    """X402ClientFlow should reject expired challenges."""
    flow = X402ClientFlow()
    challenge = PaymentChallenge.from_response({
        "recipient": ATOMADIC_TREASURY,
        "amount_micro_usdc": 1000,
        "expires": 1,  # Already expired
    })
    assert not flow.can_pay(challenge)
    assert "expired" in flow.last_error.lower()
