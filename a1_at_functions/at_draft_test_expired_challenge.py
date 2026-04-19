# Extracted from C:/!ass-ade/tests/test_x402_flow.py:72
# Component id: at.source.ass_ade.test_expired_challenge
from __future__ import annotations

__version__ = "0.1.0"

def test_expired_challenge(self) -> None:
    c = PaymentChallenge.from_response(
        {
            "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            "amount_micro_usdc": 1,
            "expires": 1,
        }
    )
    assert c.is_expired
