# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/gap_filler.py:123
# Component id: mo.source.ass_ade.propose_components
from __future__ import annotations

__version__ = "0.1.0"

def propose_components(
    gaps: list[dict[str, Any]],
    root_id: str = "",
) -> list[ProposedComponent]:
    """Turn raw gap records from the ingestor into deduplicated tier proposals."""
    by_key: dict[str, ProposedComponent] = {}
    for gap in gaps:
        symbol = gap.get("source_symbol") or {}
        name = str(symbol.get("name") or "")
        if not name or name.startswith("_"):
            continue
        tier = gap.get("tier") or "a1_at_functions"
        categories = _normalize_categories(gap.get("product_categories"))
        dkey = _dedup_key(tier, name, categories)
        cid = gap.get("candidate_id") or (
            f"{_tier_prefix(tier)}.source.{_slug(root_id)}.{_slug(name)}"
        )
        prop = ProposedComponent(
            id=cid,
            tier=tier,
            kind=_kind_for(tier, str(symbol.get("kind") or "")),
            name=name,
            source_symbol=symbol,
            product_categories=categories,
            description=f"Draft candidate from {symbol.get('path', '')}:{symbol.get('line', 0)}.",
            dedup_key=dkey,
        )
        incumbent = by_key.get(dkey)
        if incumbent is None or _proposal_sort_key(prop) < _proposal_sort_key(incumbent):
            by_key[dkey] = prop
    return sorted(by_key.values(), key=_proposal_sort_key)
