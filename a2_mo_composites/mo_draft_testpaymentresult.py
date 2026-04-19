# Extracted from C:/!ass-ade/tests/test_x402_flow.py:306
# Component id: mo.source.ass_ade.testpaymentresult
from __future__ import annotations

__version__ = "0.1.0"

class TestPaymentResult:
    def test_build_header_success(self) -> None:
        r = PaymentResult(success=True, txid="abc123", signature_header="sig;pk;txid;8000")
        headers = build_payment_header(r)
        assert "PAYMENT-SIGNATURE" in headers
        assert headers["PAYMENT-SIGNATURE"] == "sig;pk;txid;8000"

    def test_build_header_failure(self) -> None:
        r = PaymentResult(success=False, error="no wallet")
        headers = build_payment_header(r)
        assert headers == {}
