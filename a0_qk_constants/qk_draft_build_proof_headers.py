# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:452
# Component id: qk.source.ass_ade.build_proof_headers
from __future__ import annotations

__version__ = "0.1.0"

def build_proof_headers(self, payment: PaymentResult) -> dict[str, str]:
    """Build HTTP headers from a successful payment for request retry."""
    return build_payment_header(payment)
