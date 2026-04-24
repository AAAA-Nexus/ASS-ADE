"""Tier a1 — assimilated function 'propose_components'

Assimilated from: rebuild/gap_filler.py:112-142
"""

from __future__ import annotations


# --- assimilated symbol ---
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

