"""Tier a1 — assimilated function 'assess_blueprint_fulfillment'

Assimilated from: rebuild/gap_filler.py:207-258
"""

from __future__ import annotations


# --- assimilated symbol ---
def assess_blueprint_fulfillment(
    blueprints: list[dict[str, Any]],
    proposals: list[ProposedComponent],
    registry: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """For every blueprint, tag each required component as registry / proposal / missing."""
    registry_ids = _registry_ids(registry)
    out: list[dict[str, Any]] = []
    for bp in blueprints:
        required_ids: list[str] = []
        requirement_metadata: dict[str, dict[str, Any]] = {}
        root = bp.get("root_component")
        if root:
            required_ids.append(str(root))
        for rid in bp.get("include_components") or []:
            required_ids.append(str(rid))
        for comp in bp.get("components") or []:
            cid = _blueprint_requirement_id(comp)
            if not cid:
                continue
            if cid not in required_ids:
                required_ids.append(cid)
            if isinstance(comp, dict):
                requirement_metadata[cid] = _blueprint_requirement_metadata(comp, cid)
        satisfied_registry: list[str] = []
        satisfied_proposal: list[dict[str, str]] = []
        missing: list[str] = []
        for rid in required_ids:
            status, matched = _match_blueprint(rid, proposals, registry_ids)
            if status == "registry":
                satisfied_registry.append(rid)
            elif status == "proposal":
                satisfied_proposal.append({"required": rid, "proposal": matched or ""})
            else:
                missing.append(rid)
        missing_metadata = {
            rid: requirement_metadata[rid]
            for rid in missing
            if rid in requirement_metadata
        }
        out.append({
            "blueprint_id": bp.get("id") or bp.get("blueprint_id"),
            "blueprint_name": bp.get("name") or bp.get("blueprint_name"),
            "visibility": bp.get("visibility"),
            "required_count": len(required_ids),
            "satisfied_by_registry": satisfied_registry,
            "satisfied_by_proposal": satisfied_proposal,
            "still_unfulfilled": missing,
            "still_unfulfilled_metadata": missing_metadata,
            "fully_satisfied": len(missing) == 0,
        })
    return out

