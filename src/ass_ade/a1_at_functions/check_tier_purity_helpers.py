"""Tier a1 — assimilated function 'check_tier_purity'

Assimilated from: rebuild/tier_purity.py:41-133
"""

from __future__ import annotations


# --- assimilated symbol ---
def check_tier_purity(
    plan: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Validate every proposed component against the monadic composition law.

    Returns ``{"violations": [...], "pure": bool, "by_tier": {...}}``.
    """
    components = _plan_components(plan)
    violations: list[dict[str, str]] = []
    by_tier: dict[str, dict[str, int]] = {}

    for comp in components:
        comp_id: str = comp.get("id", "<unknown>")
        comp_tier: str = comp.get("tier", "")
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
                        f"Dep '{dep}' has no recognised tier prefix "
                        "(expected '<prefix>.<name>', prefix one of a0/a1/a2/a3/a4; legacy qk/at/mo/og/sy still accepted on read)."
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

