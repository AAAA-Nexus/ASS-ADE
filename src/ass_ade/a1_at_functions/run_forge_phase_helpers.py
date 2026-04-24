"""Tier a1 — assimilated function 'run_forge_phase'

Assimilated from: rebuild/forge.py:806-849
"""

from __future__ import annotations


# --- assimilated symbol ---
def run_forge_phase(
    target_root: Path,
    model: str = _FORGE_MODEL,
    max_workers: int = _MAX_WORKERS,
) -> dict[str, Any]:
    """Full forge phase: Epiphany analysis → ForgeLoop execution.

    Returns a summary dict compatible with the orchestrator phases dict.
    """
    log.info("Phase 5b [Epiphany]: Analyzing %s …", target_root.name)
    plan = generate_plan(target_root)

    if not plan.promoted:
        log.info("Epiphany: no improvement tasks found — skipping forge")
        return {"tasks": 0, "applied": 0, "skipped": 0, "files_modified": 0}

    log.info(
        "Phase 5b [Forge]: Executing %d tasks across %d files (model=%s, workers=%d) …",
        len(plan.experiments),
        len({t.file for t in plan.experiments}),
        model,
        max_workers,
    )
    forge = execute_plan(plan, model=model, max_workers=max_workers)

    summary: dict[str, Any] = {
        "tasks": forge.plan_tasks,
        "applied": forge.applied,
        "skipped": forge.skipped,
        "files_modified": len(forge.files_modified),
        "model": forge.model_used,
        "changes": [
            {
                "file": r.file,
                "node": r.node,
                "issue": r.issue,
                "verified": r.verified,
                "summary": r.diff_summary,
                "error": r.error,
            }
            for r in forge.results
        ],
    }
    return summary

