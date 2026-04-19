# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_x402clientflow.py:89
# Component id: qk.source.a2_mo_composites.build_proof_headers
from __future__ import annotations

__version__ = "0.1.0"

def build_proof_headers(self, payment: PaymentResult) -> dict[str, str]:
    """Build HTTP headers from a successful payment for request retry."""
    return build_payment_header(payment)
