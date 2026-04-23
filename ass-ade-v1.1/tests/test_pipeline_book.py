from __future__ import annotations

from pathlib import Path

from ass_ade_v11.a3_og_features.pipeline_book import run_book_until, stop_after_from_label


def test_stop_after_from_label_is_case_insensitive() -> None:
    assert stop_after_from_label("PACKAGE") == 7
    assert stop_after_from_label("Recon") == 0


def test_run_book_until_stops_after_gapfill(minimal_pkg_root: Path) -> None:
    book = run_book_until(minimal_pkg_root, None, stop_after=2)
    assert book["stopped_after"] == 2
    assert "phase2" in book
    assert "phase3" not in book


def test_run_book_until_stops_after_validate(minimal_pkg_root: Path, tmp_path: Path) -> None:
    book = run_book_until(minimal_pkg_root, tmp_path, stop_after=4)
    assert book["stopped_after"] == 4
    assert "phase4" in book
    assert "phase5" not in book


def test_run_book_until_requires_output_for_materialize(minimal_pkg_root: Path) -> None:
    try:
        run_book_until(minimal_pkg_root, None, stop_after=5)
    except ValueError as exc:
        assert "output_parent" in str(exc).lower()
    else:
        raise AssertionError("expected ValueError")
