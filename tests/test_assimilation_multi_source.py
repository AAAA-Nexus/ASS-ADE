"""Pipeline: multiple source roots merged into one gap plan and one materialized tree."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.a3_og_features.pipeline_book import run_book_until
from ass_ade.a4_sy_orchestration.cli import app


def _a1_fixture() -> Path:
    return Path(__file__).resolve().parent / "fixtures" / "a1_only"


def test_run_book_recon_requires_python_in_every_root(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    empty = tmp_path / "no_python"
    empty.mkdir()
    book = run_book_until(
        minimal_pkg_root,
        None,
        extra_source_roots=[empty],
        stop_after=2,
    )
    assert book["stopped_after"] == 0
    assert book["phase0"]["verdict"] == "RECON_REQUIRED"
    assert len(book["phase0"].get("codebases") or []) == 2


def test_run_book_merges_two_sources_at_gapfill(minimal_pkg_root: Path, tmp_path: Path) -> None:
    book = run_book_until(
        minimal_pkg_root,
        tmp_path,
        extra_source_roots=[_a1_fixture()],
        stop_after=2,
        rebuild_tag="merge-gapfill",
    )
    assert book["stopped_after"] == 2
    assert book["phase1"]["summary"]["sources"] == 2
    assert len(book["phase1"]["ingestions"]) == 2
    n_props = len(book["phase2"]["gap_plan"]["proposed_components"])
    assert n_props >= 1


def test_materialize_writes_assimilation_log(minimal_pkg_root: Path, tmp_path: Path) -> None:
    book = run_book_until(
        minimal_pkg_root,
        tmp_path,
        extra_source_roots=[_a1_fixture()],
        stop_after=5,
        rebuild_tag="assim-out",
    )
    assert book["stopped_after"] == 5
    root = Path(book["phase5"]["target_root"])
    log_path = root / "ASSIMILATION.json"
    assert log_path.is_file()
    doc = json.loads(log_path.read_text(encoding="utf-8"))
    assert doc["assimilation_schema"] == "ASSADE-ASSIMILATION-V11"
    assert len(doc["source_roots"]) == 2
    assert doc["phase4_acyclic"] is True
    assert book["phase5"]["assimilation"] is not None


def test_cli_rebuild_with_also_merges(minimal_pkg_root: Path, tmp_path: Path) -> None:
    out = tmp_path / "book.json"
    runner = CliRunner()
    r = runner.invoke(
        app,
        [
            "rebuild",
            str(minimal_pkg_root),
            "--also",
            str(_a1_fixture()),
            "--stop-after",
            "gapfill",
            "--json-out",
            str(out),
        ],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    book = json.loads(out.read_text(encoding="utf-8"))
    assert book["phase1"]["summary"]["sources"] == 2


def test_root_ids_must_match_source_count(minimal_pkg_root: Path, tmp_path: Path) -> None:
    try:
        run_book_until(
            minimal_pkg_root,
            tmp_path,
            extra_source_roots=[_a1_fixture()],
            root_ids=["only_one"],
            stop_after=1,
        )
    except ValueError as exc:
        assert "root_ids length" in str(exc).lower()
    else:
        raise AssertionError("expected ValueError")
