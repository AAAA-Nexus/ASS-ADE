# Extracted from C:/!ass-ade/tests/test_x402_flow.py:276
# Component id: at.source.ass_ade.test_format_includes_amount
from __future__ import annotations

__version__ = "0.1.0"

def test_format_includes_amount(self) -> None:
    c = PaymentChallenge.from_response({
        "amount_usdc": "0.008000",
        "amount_micro_usdc": 8000,
        "recipient": ATOMADIC_TREASURY,
        "endpoint": "/v1/trust/score",
    })
    text = format_payment_consent(c)
    assert "$0.008000 USDC" in text
    assert "/v1/trust/score" in text
    assert ATOMADIC_TREASURY in text
