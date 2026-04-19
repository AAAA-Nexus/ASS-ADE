# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_product_categories.py:7
# Component id: at.source.a1_at_functions.product_categories
from __future__ import annotations

__version__ = "0.1.0"

def product_categories(symbol: Symbol) -> list[str]:
    haystack = f"{symbol.path} {symbol.name}".lower()
    categories: list[str] = []
    if any(term in haystack for term in ("pay", "x402", "billing", "fee", "price")):
        categories.append("PAY")
    if any(term in haystack for term in ("identity", "delegation", "trust", "ucan")):
        categories.append("IDT")
    if any(term in haystack for term in ("theorem", "rag", "search", "answer", "proof")):
        categories.append("DCM")
    if any(term in haystack for term in ("audit", "compliance", "policy", "vault")):
        categories.append("SRG")
    if any(term in haystack for term in ("security", "crypto", "pqc", "threat")):
        categories.append("SEC")
    if not categories:
        categories.append("COR")
    return categories
