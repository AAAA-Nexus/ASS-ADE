from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.a4_sy_orchestration.run_phases_0_2 import run_book_phases_0_2


def test_pipeline_runs_through_phase3(minimal_pkg_root: Path) -> None:
    book = run_book_phases_0_2(minimal_pkg_root)
    assert book["stopped_after"] == 3
    assert book["phase2"]["gap_plan"]["gap_fill_schema"].endswith("V11")
    assert book["phase3"]["summary"]["bodies_attached"] >= 1


def test_pipeline_stops_at_gapfill_when_enrich_disabled(minimal_pkg_root: Path) -> None:
    book = run_book_phases_0_2(minimal_pkg_root, enrich=False)
    assert book["stopped_after"] == 2
    assert "phase3" not in book


def test_pipeline_stops_when_empty(tmp_path: Path) -> None:
    book = run_book_phases_0_2(tmp_path)
    assert book["stopped_after"] == 0
    assert "phase1" not in book
