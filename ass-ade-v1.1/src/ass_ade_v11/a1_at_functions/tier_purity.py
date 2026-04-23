"""Tier purity — monadic composition law (ported from ass-ade-v1)."""

from __future__ import annotations

from typing import Any

from ass_ade_v11.a0_qk_constants.tier_names import PREFIX_TO_TIER

ALLOWED_DEP_TIERS: dict[str, set[str]] = {
    "a0_qk_constants": set(),
    "a1_at_functions": {"a0", "qk"},
    "a2_mo_composites": {"a1", "at"},
    "a3_og_features": {"a2", "mo"},
    "a4_sy_orchestration": {"a3", "og"},
}


def tier_prefix_from_id(dep_id: str) -> str | None:
    if "." not in dep_id:
        return None
    prefix = dep_id.split(".", 1)[0]
    return prefix if prefix in PREFIX_TO_TIER else None


def _plan_components(plan: dict[str, Any]) -> list[dict[str, Any]]:
    if "proposed_components" in plan:
        return plan.get("proposed_components") or []
    return plan.get("components") or []


def check_tier_purity(
    plan: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    components = _plan_components(plan)
    violations: list[dict[str, str]] = []
    by_tier: dict[str, dict[str, int]] = {}

    for comp in components:
        comp_id: str = str(comp.get("id", "<unknown>"))
        comp_tier: str = str(comp.get("tier", ""))
        made_of: list[str] = comp.get("made_of") or []

        tier_stats = by_tier.setdefault(comp_tier, {"checked": 0, "violations": 0})
        tier_stats["checked"] += 1

        if comp_tier not in ALLOWED_DEP_TIERS:
            if strict:
                if not made_of:
                    violations.append({
                        "component_id": comp_id,
                        "component_tier": comp_tier,
                        "bad_dep": "",
                        "bad_dep_tier": "unknown",
                        "reason": (
                            f"Component tier '{comp_tier}' is not in the tier table; "
                            "strict mode requires a known tier."
                        ),
                    })
                    tier_stats["violations"] += 1
                    continue
                for dep in made_of:
                    dep_prefix = tier_prefix_from_id(dep)
                    dep_tier_name = PREFIX_TO_TIER.get(dep_prefix, "unknown") if dep_prefix else "unknown"
                    violations.append({
                        "component_id": comp_id,
                        "component_tier": comp_tier,
                        "bad_dep": dep,
                        "bad_dep_tier": dep_tier_name,
                        "reason": (
                            f"Component tier '{comp_tier}' is not in the tier table; "
                            f"dep '{dep}' cannot be validated."
                        ),
                    })
                    tier_stats["violations"] += 1
            continue

        allowed_prefixes: set[str] = ALLOWED_DEP_TIERS[comp_tier]

        for dep in made_of:
            dep_prefix = tier_prefix_from_id(dep)

            if dep_prefix is None:
                violations.append({
                    "component_id": comp_id,
                    "component_tier": comp_tier,
                    "bad_dep": dep,
                    "bad_dep_tier": "unknown",
                    "reason": (
                        "Dep has no recognised tier prefix "
                        "(expected '<prefix>.<name>')."
                    ),
                })
                tier_stats["violations"] += 1
                continue

            if dep_prefix in allowed_prefixes:
                continue

            dep_tier_name = PREFIX_TO_TIER.get(dep_prefix, "unknown")
            allowed_str = ", ".join(sorted(allowed_prefixes)) if allowed_prefixes else "nothing"
            violations.append({
                "component_id": comp_id,
                "component_tier": comp_tier,
                "bad_dep": dep,
                "bad_dep_tier": dep_tier_name,
                "reason": (
                    f"Tier '{comp_tier}' may only depend on [{allowed_str}]; "
                    f"dep '{dep}' belongs to tier '{dep_tier_name}'."
                ),
            })
            tier_stats["violations"] += 1

    return {
        "violations": violations,
        "pure": len(violations) == 0,
        "by_tier": by_tier,
    }


def enforce_tier_purity(plan: dict[str, Any]) -> dict[str, Any]:
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
        comp_id = str(comp.get("id", "<unknown>"))
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
