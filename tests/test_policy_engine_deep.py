"""Engine-deep tests: validated assimilate policy actually constrains ingest (Slice A)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from ass_ade.a1_at_functions.assimilate_policy_plan import build_policy_plan
from ass_ade.a1_at_functions.ingest import ingest_project, iter_source_files
from ass_ade.a3_og_features.phase1_ingest import run_phase1_ingest_multi
from ass_ade.a3_og_features.pipeline_book import run_book_until
from ass_ade.a4_sy_orchestration.unified_cli import app as unified_app


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _copy_fixture(src: Path, dst: Path) -> Path:
    shutil.copytree(src, dst)
    return dst


@pytest.mark.usecase
def test_forbid_glob_excludes_matching_file(tmp_path: Path) -> None:
    """``forbid_globs`` drops files from ``iter_source_files`` and ``ingest_project``."""
    root = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "pkg")
    secret = root / "example_pkg" / "_secret_helpers.py"
    secret.write_text(
        '"""Tier a1 — should be excluded."""\n\n\ndef classified(value: int) -> int:\n    return value\n',
        encoding="utf-8",
    )

    baseline = [p.name for p in iter_source_files(root)]
    assert "_secret_helpers.py" in baseline, "precondition: file is walked without policy"

    filtered = [
        p.name
        for p in iter_source_files(root, forbid_globs=("**/_secret_*.py",))
    ]
    assert "_secret_helpers.py" not in filtered

    policy = {
        "role": "map",
        "license_class": "compatible_oss",
        "forbid_globs": ("**/_secret_*.py",),
        "allow_globs": None,
        "max_file_bytes": 2_000_000,
        "binary_handling": "forbid",
    }
    ingested = ingest_project(root, root_id="pkg", policy=policy)
    names = {Path(s["path"]).name for s in ingested["symbols"]}
    assert "_secret_helpers.py" not in names
    assert ingested["policy_applied"]["forbid_globs"] == ["**/_secret_*.py"]


@pytest.mark.usecase
def test_forbid_glob_double_star_matches_root_level_tests_dir(tmp_path: Path) -> None:
    """Patterns like ``**/tests/**`` also catch a top-level ``tests/`` tree."""
    root = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "pkg")
    tests_dir = root / "tests"
    tests_dir.mkdir()
    test_file = tests_dir / "test_sample.py"
    test_file.write_text("def test_one() -> None:\n    assert True\n", encoding="utf-8")

    baseline = [p.as_posix() for p in iter_source_files(root)]
    assert test_file.as_posix() in baseline

    filtered = [
        p.as_posix()
        for p in iter_source_files(root, forbid_globs=("**/tests/**",))
    ]
    assert test_file.as_posix() not in filtered


@pytest.mark.usecase
def test_max_file_bytes_skips_reads(tmp_path: Path) -> None:
    """``max_file_bytes=1`` causes ``ingest_project`` to skip reading real sources."""
    root = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "pkg")
    policy = {
        "role": "map",
        "license_class": "compatible_oss",
        "forbid_globs": (),
        "allow_globs": None,
        "max_file_bytes": 1,
        "binary_handling": "forbid",
    }
    ingested = ingest_project(root, root_id="pkg", policy=policy)
    assert ingested["summary"]["symbols"] == 0
    assert ingested["policy_applied"]["max_file_bytes"] == 1


@pytest.mark.usecase
def test_build_policy_plan_resolves_only_listed_roots(tmp_path: Path) -> None:
    """Plan maps listed roots; unlisted roots stay absent (legacy path)."""
    primary = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "primary")
    sibling = _copy_fixture(FIXTURES / "cross_lib", tmp_path / "sibling")
    other = _copy_fixture(FIXTURES / "cross_app", tmp_path / "other")

    doc = {
        "schema_version": "1",
        "primary": {"role": "map", "path": str(primary)},
        "roots": [
            {
                "path": str(primary),
                "role": "map",
                "license_class": "compatible_oss",
                "forbid_globs": ["**/core.py"],
            },
            {
                "path": str(sibling),
                "role": "sibling",
                "license_class": "compatible_oss",
                "max_file_bytes": 123,
            },
        ],
    }
    plan = build_policy_plan(doc, [primary, sibling, other])
    assert primary.resolve() in plan
    assert sibling.resolve() in plan
    assert other.resolve() not in plan
    assert plan[primary.resolve()]["forbid_globs"] == ("**/core.py",)
    assert plan[sibling.resolve()]["max_file_bytes"] == 123


@pytest.mark.usecase
def test_phase1_multi_applies_per_root_policy(tmp_path: Path) -> None:
    """Phase 1 multi threads per-root policy; forbid on one root leaves others untouched."""
    primary = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "primary")
    sibling = _copy_fixture(FIXTURES / "cross_lib", tmp_path / "sibling")

    plan: dict[Path, Any] = {
        primary.resolve(): {
            "role": "map",
            "license_class": "compatible_oss",
            "forbid_globs": ("**/core.py",),
            "allow_globs": None,
            "max_file_bytes": 2_000_000,
            "binary_handling": "forbid",
        }
    }
    p1 = run_phase1_ingest_multi([primary, sibling], policy_by_root=plan)
    primary_ing = p1["ingestions"][0]
    sibling_ing = p1["ingestions"][1]

    primary_names = {Path(s["path"]).name for s in primary_ing["symbols"]}
    assert "core.py" not in primary_names

    sibling_names = {Path(s["path"]).name for s in sibling_ing["symbols"]}
    assert "util.py" in sibling_names
    assert sibling_ing["policy_applied"] is None


@pytest.mark.usecase
def test_run_book_until_propagates_policy_doc(tmp_path: Path) -> None:
    """``run_book_until(policy_doc=...)`` makes phase1 drop ``core.py`` from the primary."""
    primary = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "primary")
    sibling = _copy_fixture(FIXTURES / "cross_lib", tmp_path / "sibling")
    policy_doc = {
        "schema_version": "1",
        "primary": {"role": "map", "path": str(primary)},
        "roots": [
            {
                "path": str(primary),
                "role": "map",
                "license_class": "compatible_oss",
                "forbid_globs": ["**/core.py"],
            },
            {
                "path": str(sibling),
                "role": "sibling",
                "license_class": "compatible_oss",
            },
        ],
    }
    book = run_book_until(
        primary,
        None,
        stop_after=1,
        extra_source_roots=[sibling],
        policy_doc=policy_doc,
    )
    ingestions = book["phase1"]["ingestions"]
    primary_names = {Path(s["path"]).name for s in ingestions[0]["symbols"]}
    assert "core.py" not in primary_names
    assert ingestions[0]["policy_applied"]["forbid_globs"] == ["**/core.py"]


@pytest.mark.usecase
def test_cli_multi_root_policy_applies_forbid_glob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end CLI: ``--policy`` forbid_globs remove symbols from emitted book."""
    monkeypatch.setenv("CI", "true")
    primary = _copy_fixture(FIXTURES / "minimal_pkg", tmp_path / "primary")
    sibling = _copy_fixture(FIXTURES / "cross_lib", tmp_path / "sibling")
    policy_yaml = "\n".join(
        [
            'schema_version: "1"',
            "primary:",
            "  role: map",
            f"  path: {json.dumps(str(primary))}",
            "roots:",
            f"  - path: {json.dumps(str(primary))}",
            "    role: map",
            "    license_class: compatible_oss",
            '    forbid_globs: ["**/core.py"]',
            f"  - path: {json.dumps(str(sibling))}",
            "    role: sibling",
            "    license_class: compatible_oss",
            "",
        ]
    )
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(policy_yaml, encoding="utf-8")

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    book_json = tmp_path / "book.json"
    plan_json = tmp_path / "ASSIMILATE_PLAN.json"

    runner = CliRunner()
    r = runner.invoke(
        unified_app,
        [
            "assimilate",
            str(primary),
            str(out_dir),
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

    book = json.loads(book_json.read_text(encoding="utf-8"))
    primary_ing = book["phase1"]["ingestions"][0]
    primary_names = {Path(s["path"]).name for s in primary_ing["symbols"]}
    assert "core.py" not in primary_names
    assert primary_ing["policy_applied"]["forbid_globs"] == ["**/core.py"]
