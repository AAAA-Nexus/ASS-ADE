"""Phase 2 — gap-fill plan from one or more ingestions."""

from __future__ import annotations

from typing import Any

from ass_ade.a1_at_functions.gap_fill import build_gap_fill_plan


def run_phase2_gapfill(
    ingestions: list[dict[str, Any]],
    *,
    blueprints: list[dict[str, Any]] | None = None,
    registry: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    plan = build_gap_fill_plan(ingestions, blueprints=blueprints, registry=registry)
    return {
        "phase": 2,
        "gap_plan": plan,
        "summary": plan["summary"],
    }
