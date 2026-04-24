"""Tier a2 — assimilated class 'ProposedComponent'

Assimilated from: rebuild/gap_filler.py:26-36
"""

from __future__ import annotations


# --- assimilated symbol ---
class ProposedComponent:
    id: str
    tier: str
    kind: str
    name: str
    source_symbol: dict[str, Any]
    product_categories: list[str]
    fulfills_blueprints: list[str] = field(default_factory=list)
    made_of: list[str] = field(default_factory=list)
    description: str = ""
    dedup_key: str = ""

