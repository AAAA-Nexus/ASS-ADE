# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testx402clientflow.py:89
# Component id: qk.source.a2_mo_composites.test_get_proof
from __future__ import annotations

__version__ = "0.1.0"

def test_get_proof(self) -> None:
    """X402ClientFlow should extract PaymentProof from result."""
    flow = X402ClientFlow()
    result = PaymentResult(
        success=True,
        txid="0xabc",
        signature_header="sig;0x1234;0xabc;5000",
    )
    proof = flow.get_proof(result)
    assert proof is not None
    assert proof.wallet_address == "0x1234"
