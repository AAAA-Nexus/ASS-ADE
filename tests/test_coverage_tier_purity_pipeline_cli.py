"""tier_purity, pipeline_book, phase0, CLI, orchestration runners — coverage gaps."""

from __future__ import annotations

import builtins
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.a0_qk_constants.reference_roots import ASS_ADE_V1_REFERENCE_ROOT_ENV
from ass_ade.a1_at_functions.tier_purity import check_tier_purity, enforce_tier_purity, tier_prefix_from_id
from ass_ade.a3_og_features.phase0_recon import run_phase0_recon
from ass_ade.a3_og_features.pipeline_book import run_book_until, stop_after_from_label
from ass_ade.a3_og_features.pipeline_phases_0_2 import (
    run_phases_0_through_2,
    run_phases_0_through_3,
)
from ass_ade.a4_sy_orchestration.cli import app
from ass_ade.a4_sy_orchestration.run_phases_0_2 import run_book_phases_0_3
from ass_ade.a4_sy_orchestration.run_phases_0_2_a0 import run_book_phases_0_2_a0


def test_tier_prefix_and_plan_components_variants() -> None:
    assert tier_prefix_from_id("nope") is None
    plain = check_tier_purity({"components": [{"id": "x", "tier": "a1_at_functions", "made_of": []}]})
    assert plain["pure"] is True


def test_tier_purity_unknown_tier_strict_paths() -> None:
    bad_tier_empty = check_tier_purity(
        {"proposed_components": [{"id": "z", "tier": "bogus", "made_of": []}]},
        strict=True,
    )
    assert any("tier table" in v["reason"] for v in bad_tier_empty["violations"])

    bad_tier_deps = check_tier_purity(
        {
            "proposed_components": [
                {"id": "z", "tier": "bogus", "made_of": ["a1.helper"]},
            ],
        },
        strict=True,
    )
    assert bad_tier_deps["violations"]


def test_tier_purity_dep_prefix_none_and_illegal_edge() -> None:
    no_prefix = check_tier_purity(
        {
            "proposed_components": [
                {"id": "a1.a", "tier": "a1_at_functions", "made_of": ["naked"]},
            ],
        },
    )
    assert any("no recognised tier prefix" in v["reason"] for v in no_prefix["violations"])

    illegal = check_tier_purity(
        {
            "proposed_components": [
                {
                    "id": "a1.a",
                    "tier": "a1_at_functions",
                    "made_of": ["a2.not_allowed_for_a1"],
                },
            ],
        },
    )
    assert not illegal["pure"]


def test_enforce_tier_purity_noop_and_fix() -> None:
    clean = {"proposed_components": [{"id": "a1.a", "tier": "a1_at_functions", "made_of": []}]}
    assert enforce_tier_purity(dict(clean))["removed_edges"] == 0

    dirty = {
        "proposed_components": [
            {"id": "a1.a", "tier": "a1_at_functions", "made_of": ["a2.x"]},
            {"id": "a2.x", "tier": "a2_mo_composites", "made_of": []},
        ],
    }
    rep = enforce_tier_purity(dirty)
    assert rep["removed_edges"] >= 1
    assert dirty["summary"]["tier_purity_fixes"]


def test_phase0_recon_not_a_directory(tmp_path: Path) -> None:
    f = tmp_path / "nope.txt"
    f.write_text("x", encoding="utf-8")
    p0 = run_phase0_recon(f)
    assert p0["verdict"] == "RECON_REQUIRED"
    assert p0["codebase"].get("error") == "not_a_directory"


def test_stop_after_from_label_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown stop-after"):
        stop_after_from_label("nope")


def test_run_book_until_invalid_stop_after(minimal_pkg_root: Path) -> None:
    with pytest.raises(ValueError, match="stop_after"):
        run_book_until(minimal_pkg_root, None, stop_after=8)


def test_run_book_until_stops_phase0_only_when_ready(minimal_pkg_root: Path) -> None:
    book = run_book_until(minimal_pkg_root, None, stop_after=0)
    assert book["stopped_after"] == 0
    assert book["phase0"]["verdict"] == "READY_FOR_PHASE_1"


def test_run_book_until_stops_after_materialize_phase5(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    b5 = run_book_until(
        minimal_pkg_root, tmp_path, stop_after=5, rebuild_tag="cov_p5_only"
    )
    assert b5["stopped_after"] == 5
    assert "phase5" in b5


def test_run_book_until_stops_after_enrich_and_audit(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    b3 = run_book_until(minimal_pkg_root, tmp_path, stop_after=3)
    assert b3["stopped_after"] == 3
    assert "phase3" in b3

    b6 = run_book_until(minimal_pkg_root, tmp_path, stop_after=6, rebuild_tag="cov_audit")
    assert b6["stopped_after"] == 6
    assert "phase6" in b6


def test_run_phases_0_through_3_alias(minimal_pkg_root: Path) -> None:
    book = run_phases_0_through_3(minimal_pkg_root)
    assert book["stopped_after"] == 3


def test_run_phases_0_through_2_stops_before_enrich(minimal_pkg_root: Path) -> None:
    book = run_phases_0_through_2(minimal_pkg_root, enrich=False)
    assert book["stopped_after"] == 2
    assert "phase3" not in book


def test_run_phases_0_through_2_infers_root_id_when_single_root(
    minimal_pkg_root: Path,
) -> None:
    """When root_ids is omitted and len(roots)==1, pipeline promotes root_id to eff_root_ids."""
    book = run_phases_0_through_2(
        minimal_pkg_root,
        root_id="cov_primary",
        enrich=False,
    )
    assert book["stopped_after"] == 2
    assert book["phase1"]["ingestions"][0]["root_id"] == "cov_primary"


def test_run_phases_0_through_2_root_ids_length_mismatch(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    other = tmp_path / "o"
    other.mkdir()
    (other / "m.py").write_text("def f():\n    pass\n", encoding="utf-8")
    with pytest.raises(ValueError, match="root_ids length"):
        run_phases_0_through_2(
            minimal_pkg_root,
            extra_source_roots=[other],
            root_ids=["a"],
        )


def test_run_book_phases_0_3_wrapper(minimal_pkg_root: Path) -> None:
    book = run_book_phases_0_3(minimal_pkg_root)
    assert book["stopped_after"] == 3


def test_run_book_phases_0_2_a0_early_stop(tmp_path: Path) -> None:
    book = run_book_phases_0_2_a0(tmp_path, tmp_path / "out")
    assert book.get("a0_materialize") is None


@pytest.mark.cli
def test_cli_version_and_import_error_path(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["--version"])
    assert r.exit_code == 0
    assert r.stdout.strip()

    real_import = builtins.__import__

    def shim(name: str, globals=None, locals=None, fromlist=(), level: int = 0):  # type: ignore[no-untyped-def]
        if name == "importlib.metadata" and fromlist and "version" in fromlist:
            raise ImportError("simulated")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", shim)
    r2 = runner.invoke(app, ["--version"])
    assert r2.exit_code == 0
    err = (r2.stderr or "").lower()
    out = (r2.stdout or "").lower()
    assert "unavailable" in err or "unavailable" in out


@pytest.mark.cli
def test_cli_rebuild_json_out_and_recon_fail_exit(minimal_pkg_root: Path, tmp_path: Path) -> None:
    runner = CliRunner()
    out_json = tmp_path / "book.json"
    r = runner.invoke(
        app,
        [
            "rebuild",
            str(minimal_pkg_root),
            "--stop-after",
            "ingest",
            "--json-out",
            str(out_json),
        ],
    )
    assert r.exit_code == 0
    assert out_json.is_file()

    empty = tmp_path / "empty"
    empty.mkdir()
    r2 = runner.invoke(app, ["rebuild", str(empty), "--stop-after", "ingest"])
    assert r2.exit_code == 1


@pytest.mark.cli
def test_cli_certify_json_out(minimal_pkg_root: Path, tmp_path: Path) -> None:
    from ass_ade.a3_og_features.pipeline_book import run_book_until

    book = run_book_until(minimal_pkg_root, tmp_path, stop_after=5, rebuild_tag="cj")
    root = book["phase5"]["target_root"]
    runner = CliRunner()
    jout = tmp_path / "audit.json"
    r = runner.invoke(app, ["certify", str(root), "--json-out", str(jout)])
    assert r.exit_code == 0
    assert jout.is_file()


@pytest.mark.cli
def test_cli_rebuild_audit_nonconformant_exits_one(
    minimal_pkg_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_book(*_a: object, **_k: object) -> dict:
        return {
            "stopped_after": 6,
            "rebuild_tag": "x",
            "phase0": {"verdict": "READY_FOR_PHASE_1"},
            "phase6": {"audit": {"summary": {"structure_conformant": False}}},
        }

    monkeypatch.setattr(
        "ass_ade.a4_sy_orchestration.cli.run_book_until",
        fake_book,
    )
    runner = CliRunner()
    r = runner.invoke(
        app,
        [
            "rebuild",
            str(minimal_pkg_root),
            "--output",
            str(tmp_path),
            "--stop-after",
            "audit",
        ],
    )
    assert r.exit_code == 1


@pytest.mark.cli
def test_cli_synth_tests_emit_and_check_fail(repo_root: Path, tmp_path: Path) -> None:
    runner = CliRunner()
    r = runner.invoke(app, ["synth-tests", "--repo", str(repo_root)])
    assert r.exit_code == 0

    man = repo_root / "tests" / "generated_smoke" / "_qualnames.json"
    backup = man.read_text(encoding="utf-8")
    try:
        man.write_text("[]\n", encoding="utf-8")
        r2 = runner.invoke(app, ["synth-tests", "--check", "--repo", str(repo_root)])
        assert r2.exit_code == 1
    finally:
        man.write_text(backup, encoding="utf-8")


def test_resolve_v1_reference_root_is_dir_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ass_ade.a1_at_functions import v1_reference_index as v1

    target = tmp_path / "ref"
    target.mkdir()
    monkeypatch.setenv(ASS_ADE_V1_REFERENCE_ROOT_ENV, str(target))

    real_is_dir = Path.is_dir

    def noisy_is_dir(self: Path) -> bool:
        if self.resolve() == target.resolve():
            raise OSError("boom")
        return real_is_dir(self)

    monkeypatch.setattr(Path, "is_dir", noisy_is_dir)
    assert v1.resolve_ass_ade_v1_reference_root() is None


def test_main_py_module_invocation(repo_root: Path) -> None:
    import subprocess

    proc = subprocess.run(
        [sys.executable, "-m", "ass_ade.a4_sy_orchestration", "--help"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
        env={**__import__("os").environ, "PYTHONPATH": str(repo_root / "src")},
    )
    assert proc.returncode == 0


def test_cli_py_executed_as_script(repo_root: Path) -> None:
    cli_path = repo_root / "src" / "ass_ade" / "a4_sy_orchestration" / "cli.py"
    proc = __import__("subprocess").run(
        [sys.executable, str(cli_path), "--help"],
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "PYTHONPATH": str(repo_root / "src")},
        check=False,
    )
    assert proc.returncode == 0
    assert "rebuild" in (proc.stdout or "").lower()


def test_orchestration_dunder_main_runpy(repo_root: Path) -> None:
    import runpy

    main_py = repo_root / "src" / "ass_ade" / "a4_sy_orchestration" / "__main__.py"
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(main_py), "--help"]
        with pytest.raises(SystemExit) as excinfo:
            runpy.run_path(str(main_py), run_name="__main__")
        assert excinfo.value.code == 0
    finally:
        sys.argv = old_argv


def test_cli_module_runpy_main_guard(repo_root: Path) -> None:
    import runpy

    cli_path = repo_root / "src" / "ass_ade" / "a4_sy_orchestration" / "cli.py"
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(cli_path), "--help"]
        with pytest.raises(SystemExit) as excinfo:
            runpy.run_path(str(cli_path), run_name="__main__")
        assert excinfo.value.code == 0
    finally:
        sys.argv = old_argv
