"""Phase 0 multi-root recon edge cases."""

from __future__ import annotations

from pathlib import Path

from ass_ade.a3_og_features.phase0_recon_multi import run_phase0_recon_multi


def test_empty_roots_not_ready() -> None:
    r = run_phase0_recon_multi([], task_description="t")
    assert r["verdict"] == "RECON_REQUIRED"
    assert "at least one" in r["required_actions"][0].lower()


def test_not_a_directory(tmp_path: Path) -> None:
    f = tmp_path / "nope.txt"
    f.write_text("x", encoding="utf-8")
    r = run_phase0_recon_multi([f])
    assert r["verdict"] == "RECON_REQUIRED"
    assert any("not a directory" in x.lower() for x in r["required_actions"])


def test_directory_without_python(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    r = run_phase0_recon_multi([empty])
    assert r["verdict"] == "RECON_REQUIRED"
    assert any("no python" in x.lower() for x in r["required_actions"])


def test_single_root_includes_codebase_surface(minimal_pkg_root: Path) -> None:
    r = run_phase0_recon_multi([minimal_pkg_root])
    assert r["verdict"] == "READY_FOR_PHASE_1"
    assert r["codebase"]["python_files"] >= 1
    assert Path(r["codebase"]["root"]) == minimal_pkg_root.resolve()
