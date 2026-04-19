# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_assess_blueprint_fulfillment.py:5
# Component id: at.source.ass_ade.assess_blueprint_fulfillment
__version__ = "0.1.0"

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
        root = bp.get("root_component")
        if root:
            required_ids.append(str(root))
        for rid in bp.get("include_components") or []:
            required_ids.append(str(rid))
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
        out.append({
            "blueprint_id": bp.get("id"),
            "blueprint_name": bp.get("name"),
            "visibility": bp.get("visibility"),
            "required_count": len(required_ids),
            "satisfied_by_registry": satisfied_registry,
            "satisfied_by_proposal": satisfied_proposal,
            "still_unfulfilled": missing,
            "fully_satisfied": len(missing) == 0,
        })
    return out
