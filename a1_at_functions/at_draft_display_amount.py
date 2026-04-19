# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentchallenge.py:63
# Component id: at.source.a2_mo_composites.display_amount
from __future__ import annotations

__version__ = "0.1.0"

def display_amount(self) -> str:
    if self.amount_usdc:
        return f"${self.amount_usdc:.6f} USDC"
    return f"{self.amount_micro_usdc} micro-USDC"
