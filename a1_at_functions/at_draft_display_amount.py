# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:106
# Component id: at.source.ass_ade.display_amount
from __future__ import annotations

__version__ = "0.1.0"

def display_amount(self) -> str:
    if self.amount_usdc:
        return f"${self.amount_usdc:.6f} USDC"
    return f"{self.amount_micro_usdc} micro-USDC"
