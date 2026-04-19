# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_full_flow_payment_failure.py:7
# Component id: at.source.a1_at_functions.test_full_flow_payment_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_full_flow_payment_failure(self) -> None:
    """Full flow: challenge → failure to pay."""
    flow = X402ClientFlow()

    response_body = {
        "amount_micro_usdc": 5000,
        "amount_usdc": "0.005",
        "recipient": ATOMADIC_TREASURY,
        "expires": 1,  # Already expired
    }

    challenge = flow.parse_challenge(response_body)
    assert challenge is not None

    # Client should not proceed due to expiry
    assert not flow.can_pay(challenge)
    assert "expired" in flow.last_error.lower()
