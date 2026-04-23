from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade_v11.a4_sy_orchestration.cli import app


@pytest.mark.cli
def test_cli_help_exits_zero() -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    out = (r.stdout or r.output or "").lower()
    assert "rebuild" in out
    assert "certify" in out
    assert "synth-tests" in out


@pytest.mark.cli
def test_cli_certify_help() -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["certify", "--help"])
    assert r.exit_code == 0


@pytest.mark.cli
def test_cli_certify_empty_dir_fails(tmp_path: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["certify", str(tmp_path)])
    assert r.exit_code == 1


@pytest.mark.cli
def test_cli_synth_tests_check_passes(repo_root: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["synth-tests", "--check", "--repo", str(repo_root)])
    assert r.exit_code == 0, r.stdout + (r.stderr or "")


@pytest.mark.cli
def test_cli_certify_materialized_tree(minimal_pkg_root: Path, tmp_path: Path) -> None:
    from ass_ade_v11.a3_og_features.pipeline_book import run_book_until

    book = run_book_until(
        minimal_pkg_root,
        tmp_path,
        stop_after=5,
        rebuild_tag="cli-certify",
    )
    assert book["stopped_after"] == 5
    root = book["phase5"]["target_root"]
    runner = CliRunner()
    r = runner.invoke(app, ["certify", str(root)])
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    assert '"structure_conformant": true' in r.stdout.lower()


@pytest.mark.cli
def test_cli_rebuild_stop_after_gapfill(minimal_pkg_root: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(
        app,
        ["rebuild", str(minimal_pkg_root), "--stop-after", "gapfill"],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    assert '"stopped_after": 2' in r.stdout


@pytest.mark.cli
def test_cli_rebuild_package_requires_output(minimal_pkg_root: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(
        app,
        ["rebuild", str(minimal_pkg_root), "--stop-after", "package"],
    )
    assert r.exit_code == 2


@pytest.mark.cli
def test_cli_invalid_stop_after(minimal_pkg_root: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(
        app,
        ["rebuild", str(minimal_pkg_root), "--stop-after", "not-a-phase"],
    )
    assert r.exit_code == 2
