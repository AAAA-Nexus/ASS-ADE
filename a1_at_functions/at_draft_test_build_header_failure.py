# Extracted from C:/!ass-ade/tests/test_x402_flow.py:313
# Component id: at.source.ass_ade.test_build_header_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_build_header_failure(self) -> None:
    r = PaymentResult(success=False, error="no wallet")
    headers = build_payment_header(r)
    assert headers == {}
