# Extracted from C:/!ass-ade/tests/test_x402_flow.py:47
# Component id: at.source.ass_ade.test_from_response_full
from __future__ import annotations

__version__ = "0.1.0"

def test_from_response_full(self) -> None:
    body = {
        "x402_version": "2.1",
        "chain_id": 8453,
        "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "amount_micro_usdc": 8000,
        "amount_usdc": "0.008000",
        "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
        "nonce": "abc123",
        "expires": 9999999999,
        "endpoint": "/v1/trust/score",
    }
    c = PaymentChallenge.from_response(body)
    assert c.amount_micro_usdc == 8000
    assert c.amount_usdc == 0.008
    assert c.recipient == "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"
    assert c.chain_id == 8453
    assert c.endpoint == "/v1/trust/score"
    assert not c.is_expired
    assert "$0.008000 USDC" in c.display_amount
