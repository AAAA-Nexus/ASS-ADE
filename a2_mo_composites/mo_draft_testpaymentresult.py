# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpaymentresult.py:7
# Component id: mo.source.a2_mo_composites.testpaymentresult
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
