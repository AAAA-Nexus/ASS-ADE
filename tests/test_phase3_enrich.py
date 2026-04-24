from __future__ import annotations

import pytest

from ass_ade.a3_og_features.phase1_ingest import run_phase1_ingest
from ass_ade.a3_og_features.phase2_gapfill import run_phase2_gapfill
from ass_ade.a3_og_features.phase3_enrich import run_phase3_enrich


@pytest.mark.phase3_enrich
def test_phase3_attaches_bodies_and_made_of(minimal_pkg_root) -> None:
    p1 = run_phase1_ingest(minimal_pkg_root, root_id="fixture")
    p2 = run_phase2_gapfill([p1["ingestion"]])
    plan = p2["gap_plan"]
    p3 = run_phase3_enrich(plan)
    assert p3["summary"]["bodies_attached"] >= 1
    props = plan["proposed_components"]
    with_body = [p for p in props if p.get("body")]
    assert with_body, "expected at least one extracted body"
    caller = next((p for p in props if p.get("name") == "caller_uses_helper"), None)
    helper = next((p for p in props if p.get("name") == "pure_helper"), None)
    assert caller and helper, "fixture must expose caller_uses_helper and pure_helper"
    helper_id = str(helper["id"])
    made_of = list(caller.get("made_of") or [])
    assert helper_id in made_of, f"expected made_of edge to pure_helper, got {made_of}"
