from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade_v11.a4_sy_orchestration.unified_cli import app as unified_app


@pytest.mark.cli
def test_unified_cli_help_lists_book_and_doctor() -> None:
    runner = CliRunner()
    r = runner.invoke(unified_app, ["--help"])
    assert r.exit_code == 0
    out = (r.stdout or r.output or "").lower()
    assert "book" in out
    assert "doctor" in out
    assert "assimilate" in out
    assert "atomadic" in out


@pytest.mark.cli
def test_unified_book_delegate_help() -> None:
    runner = CliRunner()
    r = runner.invoke(unified_app, ["book", "rebuild", "--help"])
    assert r.exit_code == 0
    out = (r.stdout or r.output or "").lower()
    assert "stop-after" in out


@pytest.mark.cli
def test_unified_doctor_runs() -> None:
    runner = CliRunner()
    r = runner.invoke(unified_app, ["doctor"])
    assert r.exit_code == 0
    out = r.stdout or r.output or ""
    assert "monadic pipeline" in out.lower()
    assert "atomadic engine" in out.lower()


@pytest.mark.cli
def test_unified_atomadic_shim_forwards_build_help() -> None:
    """``ass-ade-unified atomadic …`` forwards argv to the Click ``atomadic`` group."""
    runner = CliRunner()
    r = runner.invoke(unified_app, ["atomadic", "build", "--help"])
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    out = (r.stdout or r.output or "").lower()
    assert "synthesize" in out or "build" in out


@pytest.mark.cli
def test_unified_assimilate_help() -> None:
    runner = CliRunner()
    r = runner.invoke(unified_app, ["assimilate", "--help"])
    assert r.exit_code == 0
    out = (r.stdout or r.output or "").lower()
    assert "primary" in out or "output" in out
    assert "also" in out


@pytest.mark.cli
def test_unified_assimilate_gapfill(minimal_pkg_root: Path, tmp_path: Path) -> None:
    book_json = tmp_path / "book.json"
    plan_json = tmp_path / "ASSIMILATE_PLAN.json"
    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(tmp_path),
            "--stop-after",
            "gapfill",
            "--json-out",
            str(book_json),
            "--plan-out",
            str(plan_json),
        ],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    assert '"stopped_after": 2' in r.stdout
    assert '"assimilate_plan_schema_version": "1"' in r.stdout
    book = json.loads(book_json.read_text(encoding="utf-8"))
    assert book.get("ASSIMILATE_PLAN", {}).get("schema_version") == "1"
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    assert plan.get("primary_path")


@pytest.mark.cli
def test_unified_assimilate_also_requires_policy_when_ci(
    minimal_pkg_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sibling = tmp_path / "sibling_pkg"
    shutil.copytree(minimal_pkg_root, sibling)
    monkeypatch.setenv("CI", "true")
    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(tmp_path / "out"),
            "--also",
            str(sibling),
            "--stop-after",
            "gapfill",
        ],
    )
    assert r.exit_code == 2
    err = (r.stdout or "") + (r.stderr or "")
    assert "--policy" in err.lower()


@pytest.mark.cli
def test_unified_assimilate_also_with_policy_under_ci(
    minimal_pkg_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sibling = tmp_path / "sibling_pkg"
    shutil.copytree(minimal_pkg_root, sibling)
    monkeypatch.setenv("CI", "true")
    policy_path = tmp_path / "policy.yaml"
    p = str(minimal_pkg_root.resolve())
    s = str(sibling.resolve())
    policy_path.write_text(
        "\n".join(
            [
                'schema_version: "1"',
                "primary:",
                "  role: map",
                f"  path: {json.dumps(p)}",
                "roots:",
                f"  - path: {json.dumps(p)}",
                "    role: map",
                "    license_class: compatible_oss",
                f"  - path: {json.dumps(s)}",
                "    role: sibling",
                "    license_class: compatible_oss",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(tmp_path / "out"),
            "--also",
            str(sibling),
            "--policy",
            str(policy_path),
            "--stop-after",
            "gapfill",
        ],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    assert '"stopped_after": 2' in r.stdout
    assert '"policy_schema_version": "1"' in r.stdout


@pytest.mark.cli
def test_unified_assimilate_json_out_includes_policy_when_also(
    minimal_pkg_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sibling = tmp_path / "sibling_pkg"
    shutil.copytree(minimal_pkg_root, sibling)
    monkeypatch.setenv("CI", "true")
    policy_path = tmp_path / "policy.yaml"
    p = str(minimal_pkg_root.resolve())
    s = str(sibling.resolve())
    policy_path.write_text(
        "\n".join(
            [
                'schema_version: "1"',
                "primary:",
                "  role: map",
                f"  path: {json.dumps(p)}",
                "roots:",
                f"  - path: {json.dumps(p)}",
                "    role: map",
                "    license_class: compatible_oss",
                f"  - path: {json.dumps(s)}",
                "    role: sibling",
                "    license_class: compatible_oss",
                "",
            ]
        ),
        encoding="utf-8",
    )
    out_json = tmp_path / "book.json"
    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(tmp_path / "out"),
            "--also",
            str(sibling),
            "--policy",
            str(policy_path),
            "--stop-after",
            "gapfill",
            "--json-out",
            str(out_json),
        ],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload.get("assimilate_policy", {}).get("schema_version") == "1"
