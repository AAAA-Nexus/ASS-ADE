# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpaymentconsent.py:7
# Component id: mo.source.a2_mo_composites.testpaymentconsent
from __future__ import annotations

__version__ = "0.1.0"

class TestPaymentConsent:
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
