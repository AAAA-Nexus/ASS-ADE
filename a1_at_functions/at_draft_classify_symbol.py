# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/project_parser.py:196
# Component id: at.source.ass_ade.classify_symbol
from __future__ import annotations

__version__ = "0.1.0"

def classify_symbol(
    symbol: Symbol,
    root_id: str,
    registry: list[dict[str, Any]],
) -> dict[str, Any]:
    tier = classify_tier(symbol)
    prefix = TIER_PREFIX[tier]
    match = _registry_match(symbol, registry)
    component_id = match or f"{prefix}.source.{_slug(root_id)}.{_slug(symbol.name)}"
    return {
        "source_symbol": asdict(symbol),
        "tier": tier,
        "candidate_id": component_id,
        "registry_match": match,
        "product_categories": product_categories(symbol),
        "status": "mapped" if match else "gap",
    }
