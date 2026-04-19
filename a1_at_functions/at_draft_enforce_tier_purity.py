# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_enforce_tier_purity.py:5
# Component id: at.source.ass_ade.enforce_tier_purity
__version__ = "0.1.0"

def enforce_tier_purity(plan: dict[str, Any]) -> dict[str, Any]:
    """Remove dep edges that violate the composition law. Mutates ``plan`` in place.

    Returns ``{"removed_edges": int, "components_fixed": [str, ...]}``.
    """
    result = check_tier_purity(plan, strict=True)
    violations = result["violations"]

    if not violations:
        return {"removed_edges": 0, "components_fixed": []}

    bad_deps_by_comp: dict[str, set[str]] = {}
    for v in violations:
        bad_deps_by_comp.setdefault(v["component_id"], set()).add(v["bad_dep"])

    components_fixed: list[str] = []
    removed_count = 0

    for comp in _plan_components(plan):
        comp_id = comp.get("id", "<unknown>")
        if comp_id not in bad_deps_by_comp:
            continue
        bad = bad_deps_by_comp[comp_id]
        original_deps: list[str] = comp.get("made_of", [])
        cleaned_deps = [d for d in original_deps if d not in bad]
        removed_count += len(original_deps) - len(cleaned_deps)
        comp["made_of"] = cleaned_deps
        components_fixed.append(comp_id)

    summary: dict[str, Any] = plan.setdefault("summary", {})
    fixes: list[dict[str, Any]] = summary.setdefault("tier_purity_fixes", [])
    fixes.append({
        "removed_edges": removed_count,
        "components_fixed": components_fixed,
        "violations_detail": violations,
    })

    return {"removed_edges": removed_count, "components_fixed": components_fixed}
