# Extracted from C:/!ass-ade/tests/test_x402_flow.py:288
# Component id: at.source.ass_ade.test_testnet_label
from __future__ import annotations

__version__ = "0.1.0"

def test_testnet_label(self) -> None:
    c = PaymentChallenge.from_response(
        {
            "amount_micro_usdc": 1000,
            "amount_usdc": "0.001",
            "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
        }
    )
    with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
        text = format_payment_consent(c)
    assert "TESTNET" in text
