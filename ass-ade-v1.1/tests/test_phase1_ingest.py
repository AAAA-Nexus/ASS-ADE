from __future__ import annotations

import pytest

from ass_ade_v11.a3_og_features.phase1_ingest import run_phase1_ingest


@pytest.mark.phase1_ingest
def test_phase1_ingest_finds_symbols(minimal_pkg_root) -> None:
    p1 = run_phase1_ingest(minimal_pkg_root, root_id="fixture")
    assert p1["summary"]["files_scanned"] >= 1
    assert p1["summary"]["symbols"] >= 2
    assert p1["ingestion"]["ingestion_schema"].endswith("V11")
