# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentresult.py:7
# Component id: mo.source.a2_mo_composites.paymentresult
from __future__ import annotations

__version__ = "0.1.0"

class PaymentResult:
    """Result of an x402 payment attempt."""
    success: bool
    txid: str = ""
    signature_header: str = ""
    error: str = ""
    testnet: bool = False
