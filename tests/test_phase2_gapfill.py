from __future__ import annotations

import pytest

from ass_ade.a3_og_features.phase1_ingest import run_phase1_ingest
from ass_ade.a3_og_features.phase2_gapfill import run_phase2_gapfill


@pytest.mark.phase2_gapfill
def test_phase2_plan_has_digest(minimal_pkg_root) -> None:
    p1 = run_phase1_ingest(minimal_pkg_root)
    p2 = run_phase2_gapfill([p1["ingestion"]])
    assert p2["gap_plan"]["content_digest"]
    assert len(p2["gap_plan"]["proposed_components"]) >= 1
    assert p2["summary"]["proposed_components"] >= 1
