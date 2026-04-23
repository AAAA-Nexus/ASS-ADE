"""Chain phases 0 → 1 → 2 → 3 with fail-closed stop after recon."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from ass_ade_v11.a1_at_functions.v1_reference_index import attach_v1_reference_index
from ass_ade_v11.a3_og_features.phase0_recon_multi import run_phase0_recon_multi
from ass_ade_v11.a3_og_features.phase1_ingest import run_phase1_ingest_multi
from ass_ade_v11.a3_og_features.phase2_gapfill import run_phase2_gapfill
from ass_ade_v11.a3_og_features.phase3_enrich import run_phase3_enrich
from ass_ade_v11.a3_og_features.pipeline_book import unique_source_roots


def run_phases_0_through_2(
    source_root: Path,
    *,
    extra_source_roots: Sequence[Path | str] = (),
    root_id: str | None = None,
    root_ids: list[str] | None = None,
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    task_description: str = "rebuild",
    enrich: bool = True,
    max_body_chars: int | None = None,
) -> dict[str, Any]:
    """Run recon → ingest → gap-fill → optional enrich (phase 3); stop if recon is not READY."""
    roots = unique_source_roots(Path(source_root), extra_source_roots)
    eff_root_ids: list[str] | None = root_ids
    if eff_root_ids is None and root_id is not None and len(roots) == 1:
        eff_root_ids = [root_id]
    if eff_root_ids is not None and len(eff_root_ids) != len(roots):
        raise ValueError(
            f"root_ids length ({len(eff_root_ids)}) must match unique source roots ({len(roots)})"
        )

    p0 = run_phase0_recon_multi(roots, task_description=task_description)
    if p0["verdict"] != "READY_FOR_PHASE_1":
        return attach_v1_reference_index({"stopped_after": 0, "phase0": p0})
    p1 = run_phase1_ingest_multi(roots, root_ids=eff_root_ids, registry=registry)
    p2 = run_phase2_gapfill(
        p1["ingestions"],
        blueprints=blueprints,
        registry=registry or [],
    )
    if not enrich:
        return attach_v1_reference_index(
            {"stopped_after": 2, "phase0": p0, "phase1": p1, "phase2": p2}
        )
    p3 = run_phase3_enrich(p2["gap_plan"], max_body_chars=max_body_chars)
    return attach_v1_reference_index(
        {
            "stopped_after": 3,
            "phase0": p0,
            "phase1": p1,
            "phase2": p2,
            "phase3": p3,
        }
    )


def run_phases_0_through_3(
    source_root: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias with explicit phase-3 naming (enrich=True)."""
    return run_phases_0_through_2(source_root, enrich=True, **kwargs)
