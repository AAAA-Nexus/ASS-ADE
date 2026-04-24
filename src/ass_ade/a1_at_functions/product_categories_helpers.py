"""Tier a1 — assimilated function 'product_categories'

Assimilated from: rebuild/project_parser.py:264-279
"""

from __future__ import annotations


# --- assimilated symbol ---
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

