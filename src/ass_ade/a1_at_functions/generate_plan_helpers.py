"""Tier a1 — assimilated function 'generate_plan'

Assimilated from: rebuild/forge.py:474-496
"""

from __future__ import annotations


# --- assimilated symbol ---
def generate_plan(target_root: Path) -> EpiphanyPlan:
    """Epiphany pass — scan materialized output and build improvement plan."""
    plan = EpiphanyPlan(
        idea=f"Improve materialized codebase at {target_root.name}",
        vetted_sources=[str(target_root)],
    )

    py_files = sorted(target_root.rglob("*.py"))
    for path in py_files:
        if _is_trivial_init(path):
            continue
        if path.parent == target_root and path.name == "__init__.py":
            continue
        tasks = _analyze_file(path, target_root)
        plan.experiments.extend(tasks)

    plan.promoted = len(plan.experiments) > 0
    log.info(
        "Epiphany plan: %d improvement tasks across %d files",
        len(plan.experiments),
        len({t.file for t in plan.experiments}),
    )
    return plan

