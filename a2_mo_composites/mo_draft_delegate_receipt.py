# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:508
# Component id: mo.source.ass_ade.delegate_receipt
from __future__ import annotations

__version__ = "0.1.0"

def delegate_receipt(self, receipt_id: str) -> DelegateReceipt:
    """/v1/delegate/receipt/{id} — signed delegation receipt. $0.020/call"""
    return self._get_model(f"/v1/delegate/receipt/{_pseg(receipt_id, 'receipt_id')}", DelegateReceipt)
