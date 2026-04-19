# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_proposedcomponent.py:7
# Component id: mo.source.a2_mo_composites.proposedcomponent
from __future__ import annotations

__version__ = "0.1.0"

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
