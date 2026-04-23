"""Phase 3 — attach bodies and derive made_of edges on gap-fill plan."""

from __future__ import annotations

from typing import Any

from ass_ade_v11.a1_at_functions.body_extractor import (
    derive_made_of_graph,
    enrich_components_with_bodies,
)


def run_phase3_enrich(
    gap_plan: dict[str, Any],
    *,
    max_body_chars: int | None = None,
) -> dict[str, Any]:
    """Mutates ``gap_plan`` in place (same contract as ass-ade-v1 orchestrator)."""
    enrich_components_with_bodies(gap_plan, max_body_chars=max_body_chars)
    derive_made_of_graph(gap_plan)
    bodies = sum(1 for p in gap_plan.get("proposed_components") or [] if p.get("body"))
    edges = sum(len(p.get("made_of") or []) for p in gap_plan.get("proposed_components") or [])
    return {
        "phase": 3,
        "gap_plan": gap_plan,
        "summary": {
            "bodies_attached": bodies,
            "made_of_edges": edges,
        },
    }
