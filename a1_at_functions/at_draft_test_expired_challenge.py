# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpaymentchallenge.py:33
# Component id: at.source.a2_mo_composites.test_expired_challenge
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
