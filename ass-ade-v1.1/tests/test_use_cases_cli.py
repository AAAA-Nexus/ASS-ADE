"""Operator-focused use cases — run ``pytest -m usecase`` for a fast operator QA slice.

Complements ``test_unified_cli.py`` (CLI flags and gates) with end-to-end stories and
JSON Schema proof on emitted ``ASSIMILATE_PLAN.json`` (ship plan S1/S2).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade_v11.a1_at_functions.assimilate_plan_emit import (
    default_assimilate_plan_schema_path,
    validate_assimilate_plan_jsonschema,
)
from ass_ade_v11.a4_sy_orchestration.unified_cli import app as unified_app


def _policy_two_roots_yaml(primary: Path, sibling: Path) -> str:
    p, s = str(primary.resolve()), str(sibling.resolve())
    return "\n".join(
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
    )


@pytest.mark.usecase
def test_uc_operator_smoke_doctor_then_assimilate_with_plan(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    """Fresh install story: ``doctor`` then golden single-root assimilate with book + plan."""
    runner = CliRunner()
    doctor = runner.invoke(unified_app, ["doctor"])
    assert doctor.exit_code == 0, doctor.stdout + (doctor.stderr or "")

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    book_json = tmp_path / "book.json"
    plan_json = tmp_path / "ASSIMILATE_PLAN.json"
    assim = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(out_dir),
            "--stop-after",
            "gapfill",
            "--json-out",
            str(book_json),
            "--plan-out",
            str(plan_json),
        ],
    )
    assert assim.exit_code == 0, assim.stdout + (assim.stderr or "")
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    schema = default_assimilate_plan_schema_path()
    if schema.is_file():
        validate_assimilate_plan_jsonschema(plan, schema_path=schema)
    assert plan["schema_version"] == "1"
    assert plan["extra_roots"] == []
    assert plan["book_stop_after"] == "gapfill"


@pytest.mark.usecase
def test_uc_ci_multi_root_policy_with_book_and_plan_schema(
    minimal_pkg_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CI multi-root: ``--also`` requires ``--policy``; emit book + plan validated against schema."""
    monkeypatch.setenv("CI", "true")
    sibling = tmp_path / "sibling_pkg"
    shutil.copytree(minimal_pkg_root, sibling)
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(_policy_two_roots_yaml(minimal_pkg_root, sibling), encoding="utf-8")

    dest = tmp_path / "merged_out"
    dest.mkdir()
    book_json = tmp_path / "book.json"
    plan_json = tmp_path / "ASSIMILATE_PLAN.json"

    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(minimal_pkg_root),
            str(dest),
            "--also",
            str(sibling),
            "--policy",
            str(policy_path),
            "--stop-after",
            "gapfill",
            "--json-out",
            str(book_json),
            "--plan-out",
            str(plan_json),
        ],
    )
    assert r.exit_code == 0, r.stdout + (r.stderr or "")
    assert '"policy_schema_version": "1"' in (r.stdout or "")

    book = json.loads(book_json.read_text(encoding="utf-8"))
    assert book.get("assimilate_policy", {}).get("schema_version") == "1"

    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    schema = default_assimilate_plan_schema_path()
    if schema.is_file():
        validate_assimilate_plan_jsonschema(plan, schema_path=schema)
    assert len(plan["extra_roots"]) == 1
    assert Path(plan["extra_roots"][0]).resolve() == sibling.resolve()
