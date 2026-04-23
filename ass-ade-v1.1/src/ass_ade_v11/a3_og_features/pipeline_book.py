"""Unified book runner: phases 0–7 with explicit stop-after (library API)."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Sequence

from ass_ade_v11.a1_at_functions.conflict_detector import detect_namespace_conflicts
from ass_ade_v11.a1_at_functions.assimilate_policy_plan import build_policy_plan
from ass_ade_v11.a1_at_functions.v1_reference_index import attach_v1_reference_index
from ass_ade_v11.a3_og_features.phase0_recon_multi import run_phase0_recon_multi
from ass_ade_v11.a3_og_features.phase1_ingest import run_phase1_ingest, run_phase1_ingest_multi
from ass_ade_v11.a3_og_features.phase2_gapfill import run_phase2_gapfill
from ass_ade_v11.a3_og_features.phase3_enrich import run_phase3_enrich
from ass_ade_v11.a3_og_features.phase4_validate import run_phase4_validate
from ass_ade_v11.a3_og_features.phase5_materialize import run_phase5_materialize
from ass_ade_v11.a3_og_features.phase6_audit import run_phase6_audit
from ass_ade_v11.a3_og_features.phase7_package import run_phase7_package

STOP_AFTER_PHASE: dict[str, int] = {
    "recon": 0,
    "ingest": 1,
    "gapfill": 2,
    "enrich": 3,
    "validate": 4,
    "materialize": 5,
    "audit": 6,
    "package": 7,
}

STOP_AFTER_LABELS: tuple[str, ...] = tuple(STOP_AFTER_PHASE.keys())


def unique_source_roots(
    primary: Path | str,
    extra_source_roots: Sequence[Path | str] | None = None,
) -> list[Path]:
    """Return ``[primary, ...extras]`` as resolved paths (order preserved; primary first)."""
    root = Path(primary).resolve()
    extras = [Path(p).resolve() for p in (extra_source_roots or ())]
    return [root] + extras


def stop_after_from_label(label: str) -> int:
    """Resolve CLI / config label to terminal phase index (0–7)."""
    key = (label or "").strip().lower()
    if key not in STOP_AFTER_PHASE:
        allowed = ", ".join(sorted(STOP_AFTER_PHASE))
        raise ValueError(f"Unknown stop-after {label!r}; expected one of: {allowed}")
    return STOP_AFTER_PHASE[key]


def run_book_until(
    source_root: Path,
    output_parent: Path | None,
    *,
    stop_after: int = 7,
    rebuild_tag: str | None = None,
    root_id: str | None = None,
    root_ids: list[str] | None = None,
    extra_source_roots: list[Path] | None = None,
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    task_description: str = "rebuild",
    max_body_chars: int | None = None,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    distribution_name: str = "ass-ade-rebuilt-v11",
    policy_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run pipeline phases 0..``stop_after`` (inclusive). ``stop_after`` in 0..7.

    Phases 5–7 require ``output_parent`` (materialization root). Earlier phases do not.
    Each book includes ``reference_ass_ade_v1`` (MAP=TERRAIN probe for ``ass-ade-v1*``).

    Phase 0 recon runs on **every** source root (primary plus ``extra_source_roots``): each
    must be a directory with at least one ``.py`` file (after exclusions).

    When ``extra_source_roots`` is set, the first root (``source_root``) is the **primary**
    MAP terrain; additional roots merge into one gap plan (primary wins on duplicate symbols).

    When ``policy_doc`` is a validated assimilate policy, its ``roots[]`` rows are resolved
    into per-root ingest rules (``forbid_globs`` / ``allow_globs`` / ``max_file_bytes``) and
    applied to phase 1. Unmatched roots keep default (legacy) behavior.
    """
    return attach_v1_reference_index(
        _run_book_until_core(
            source_root,
            output_parent,
            stop_after=stop_after,
            rebuild_tag=rebuild_tag,
            root_id=root_id,
            root_ids=root_ids,
            extra_source_roots=extra_source_roots,
            registry=registry,
            blueprints=blueprints,
            task_description=task_description,
            max_body_chars=max_body_chars,
            break_cycles_if_found=break_cycles_if_found,
            enforce_purity=enforce_purity,
            distribution_name=distribution_name,
            policy_doc=policy_doc,
        )
    )


def _run_book_until_core(
    source_root: Path,
    output_parent: Path | None,
    *,
    stop_after: int = 7,
    rebuild_tag: str | None = None,
    root_id: str | None = None,
    root_ids: list[str] | None = None,
    extra_source_roots: list[Path] | None = None,
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    task_description: str = "rebuild",
    max_body_chars: int | None = None,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    distribution_name: str = "ass-ade-rebuilt-v11",
    policy_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if stop_after < 0 or stop_after > 7:
        raise ValueError("stop_after must be between 0 and 7")
    if stop_after >= 5 and output_parent is None:
        raise ValueError("output_parent is required when stop_after >= 5 (materialize)")

    all_roots = unique_source_roots(source_root, extra_source_roots)
    primary = all_roots[0]

    if root_ids is not None and len(root_ids) != len(all_roots):
        raise ValueError(
            f"root_ids length ({len(root_ids)}) must match number of source roots ({len(all_roots)})"
        )

    tag = rebuild_tag or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_base: Path | None = Path(output_parent).resolve() if output_parent is not None else None

    p0 = run_phase0_recon_multi(all_roots, task_description=task_description)
    if p0["verdict"] != "READY_FOR_PHASE_1":
        return {"stopped_after": 0, "phase0": p0, "rebuild_tag": tag}
    if stop_after <= 0:
        return {"stopped_after": 0, "phase0": p0, "rebuild_tag": tag}

    if len(all_roots) == 1:
        rid = root_ids[0] if root_ids else root_id
        p1 = run_phase1_ingest(
            primary,
            root_id=rid,
            registry=registry,
            policy_by_root=build_policy_plan(policy_doc, all_roots),
        )
    else:
        _policy_plan = build_policy_plan(policy_doc, all_roots)
        p1 = run_phase1_ingest_multi(
            all_roots,
            root_ids=root_ids,
            registry=registry,
            policy_by_root=_policy_plan,
        )
        p1["namespace_conflicts"] = detect_namespace_conflicts(
            all_roots,
            policy_by_root=_policy_plan or None,
        )

    if stop_after <= 1:
        return {"stopped_after": 1, "phase0": p0, "phase1": p1, "rebuild_tag": tag}

    p2 = run_phase2_gapfill(
        p1["ingestions"],
        blueprints=blueprints,
        registry=registry or [],
    )
    if stop_after <= 2:
        return {"stopped_after": 2, "phase0": p0, "phase1": p1, "phase2": p2, "rebuild_tag": tag}

    p3 = run_phase3_enrich(p2["gap_plan"], max_body_chars=max_body_chars)
    if stop_after <= 3:
        return {
            "stopped_after": 3,
            "phase0": p0,
            "phase1": p1,
            "phase2": p2,
            "phase3": p3,
            "rebuild_tag": tag,
        }

    gap_plan = p3["gap_plan"]
    p4 = run_phase4_validate(
        gap_plan,
        break_cycles_if_found=break_cycles_if_found,
        enforce_purity=enforce_purity,
    )
    if stop_after <= 4:
        return {
            "stopped_after": 4,
            "phase0": p0,
            "phase1": p1,
            "phase2": p2,
            "phase3": p3,
            "phase4": p4,
            "rebuild_tag": tag,
        }

    assert out_base is not None  # enforced by stop_after >= 5 + output_parent check above

    assimilation_meta: dict[str, Any] | None = None
    if len(all_roots) > 1:
        assimilation_meta = {
            "source_roots": [p.as_posix() for p in all_roots],
            "primary_root": primary.as_posix(),
            "namespace_conflicts": p1.get("namespace_conflicts"),
            "phase4_acyclic": bool((p4.get("cycles") or {}).get("acyclic")),
        }

    p5 = run_phase5_materialize(
        gap_plan,
        out_base,
        tag,
        assimilation_meta=assimilation_meta,
        source_roots=all_roots if len(all_roots) > 1 else None,
    )
    if stop_after <= 5:
        return {
            "stopped_after": 5,
            "phase0": p0,
            "phase1": p1,
            "phase2": p2,
            "phase3": p3,
            "phase4": p4,
            "phase5": p5,
            "rebuild_tag": tag,
        }

    target_root = Path(p5["target_root"])
    p6 = run_phase6_audit(target_root)
    if stop_after <= 6:
        return {
            "stopped_after": 6,
            "phase0": p0,
            "phase1": p1,
            "phase2": p2,
            "phase3": p3,
            "phase4": p4,
            "phase5": p5,
            "phase6": p6,
            "rebuild_tag": tag,
        }

    p7 = run_phase7_package(
        target_root,
        distribution_name=distribution_name,
        gap_plan=gap_plan,
    )
    return {
        "stopped_after": 7,
        "phase0": p0,
        "phase1": p1,
        "phase2": p2,
        "phase3": p3,
        "phase4": p4,
        "phase5": p5,
        "phase6": p6,
        "phase7": p7,
        "rebuild_tag": tag,
    }
