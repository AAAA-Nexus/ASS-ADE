# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpaymentresult.py:14
# Component id: at.source.a2_mo_composites.test_build_header_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_build_header_failure(self) -> None:
    r = PaymentResult(success=False, error="no wallet")
    headers = build_payment_header(r)
    assert headers == {}
