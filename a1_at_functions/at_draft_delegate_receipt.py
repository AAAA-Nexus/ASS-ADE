# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_delegate_receipt.py:7
# Component id: at.source.a1_at_functions.delegate_receipt
from __future__ import annotations

__version__ = "0.1.0"

def delegate_receipt(self, receipt_id: str) -> DelegateReceipt:
    """/v1/delegate/receipt/{id} — signed delegation receipt. $0.020/call"""
    return self._get_model(f"/v1/delegate/receipt/{_pseg(receipt_id, 'receipt_id')}", DelegateReceipt)
