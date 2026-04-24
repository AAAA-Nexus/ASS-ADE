"""Tier a3 — phase 5b: detect and fix upward import violations in materialized output.

Sits between phase 5 (materialize) and phase 6 (audit).  Uses the
ContextLoaderWiringSpecialist to scan the materialized tree for any upward
tier imports left by the CNA rewriter and patches them in-place.

Also exposes wiring_burst_task() so the fractal subagent system can invoke
wiring as a parallel burst across file groups.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade_v11.a1_at_functions.fractal_subagent_lifecycle import (
    preload_context,
    run_burst_lifecycle,
)
from ass_ade_v11.a2_mo_composites.context_loader_wiring_specialist_core import (
    ContextLoaderWiringSpecialist,
)


# ---------------------------------------------------------------------------
# Fractal burst task
# ---------------------------------------------------------------------------

def wiring_burst_task(context: dict[str, Any]) -> dict[str, Any]:
    """Burst-task wrapper: wire a single source directory and return receipts.

    Expected payload keys:
      - source_dir   (str) : directory to scan and patch
      - package_name (str | None) : optional package prefix for generated imports
    """
    payload = context.get("payload", {})
    source_dir: str = payload.get("source_dir", "")
    package_name: str | None = payload.get("package_name")

    specialist = ContextLoaderWiringSpecialist(package_name=package_name)
    report = specialist.wire(source_dir)

    return {
        "result": report,
        "receipts": {
            "wiring_phase": "complete",
            "files_changed": report.get("files_changed", 0),
            "violations_found": report.get("violations_found", 0),
            "auto_fixed": report.get("auto_fixed", 0),
            "verdict": report.get("verdict", "UNKNOWN"),
        },
    }


# ---------------------------------------------------------------------------
# Pipeline phase
# ---------------------------------------------------------------------------

def run_phase5b_wire(
    target_root: Path,
    *,
    package_name: str | None = None,
    parent_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Phase 5b — wire imports in the materialized output tree.

    Runs ContextLoaderWiringSpecialist across target_root, fixing any upward
    import violations that were not resolved during phase 5 materialization.

    Returns a phase report dict with:
      - phase            : "5b_wire"
      - target_root      : directory scanned
      - violations_found : total violations detected
      - auto_fixed       : import statements rewritten on disk
      - not_fixable      : violations requiring manual intervention
      - files_changed    : number of files patched
      - manual_review    : list of violation dicts needing human attention
      - verdict          : "PASS" | "REFINE"
    """
    parent_ctx: dict[str, Any] = parent_context or {"receipts": {}}
    payload: dict[str, Any] = {
        "source_dir": str(target_root),
        "package_name": package_name,
    }
    ctx = preload_context(parent_ctx, payload, "a3.phase5b.wire")
    result = run_burst_lifecycle(wiring_burst_task, ctx)
    report: dict[str, Any] = result.get("result", {})

    return {
        "phase": "5b_wire",
        "target_root": str(target_root),
        "violations_found": report.get("violations_found", 0),
        "auto_fixed": report.get("auto_fixed", 0),
        "not_fixable": report.get("not_fixable", 0),
        "files_changed": report.get("files_changed", 0),
        "manual_review": report.get("manual_review", []),
        "verdict": report.get("verdict", "UNKNOWN"),
    }
