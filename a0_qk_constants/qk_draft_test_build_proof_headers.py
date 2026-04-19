# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testx402clientflow.py:77
# Component id: qk.source.a2_mo_composites.test_build_proof_headers
from __future__ import annotations

__version__ = "0.1.0"

def test_build_proof_headers(self) -> None:
    """X402ClientFlow should build proof headers from payment result."""
    flow = X402ClientFlow()
    result = PaymentResult(
        success=True,
        txid="0xabc",
        signature_header="sig;0x1234;0xabc;5000",
    )
    headers = flow.build_proof_headers(result)
    assert "PAYMENT-SIGNATURE" in headers
    assert headers["PAYMENT-SIGNATURE"] == "sig;0x1234;0xabc;5000"
