"""Branch coverage for audit_rebuild, materialize_tiers, repo_stats."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from ass_ade_v11.a0_qk_constants.schemas import COMPONENT_SCHEMA_V11
from ass_ade_v11.a1_at_functions.audit_rebuild import validate_rebuild_v11
from ass_ade_v11.a1_at_functions.materialize_tiers import materialize_gap_plan_to_tree
from ass_ade_v11.a1_at_functions.repo_stats import compute_repo_surface, _walk_top_level_dirs


def test_validate_rebuild_missing_root(tmp_path: Path) -> None:
    missing = tmp_path / "nope"
    r = validate_rebuild_v11(missing)
    assert r["validated"] is False
    assert "does not exist" in r["reason"]


def test_validate_rebuild_json_parse_error(tmp_path: Path) -> None:
    root = tmp_path / "out"
    tier = root / "a1_at_functions"
    tier.mkdir(parents=True)
    (tier / "bad.json").write_text("{", encoding="utf-8")
    r = validate_rebuild_v11(root)
    assert r["validated"] is True
    assert any(f.get("code") == "JSON_PARSE" for f in r["findings"])


def test_validate_rebuild_missing_field_and_tier_issues(tmp_path: Path) -> None:
    root = tmp_path / "out"
    tier = root / "a1_at_functions"
    tier.mkdir(parents=True)
    incomplete = {"id": "a1.x", "tier": "a1_at_functions"}
    (tier / "a.json").write_text(json.dumps(incomplete), encoding="utf-8")

    wrong_tier = {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": "a1.ok",
        "tier": "not_a_real_tier",
        "name": "n",
        "kind": "k",
        "description": "d",
        "made_of": [],
        "provides": [],
        "reuse_policy": "r",
        "status": "s",
    }
    (tier / "b.json").write_text(json.dumps(wrong_tier), encoding="utf-8")

    prefix_bad = {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": "wrong.prefix",
        "tier": "a1_at_functions",
        "name": "n",
        "kind": "k",
        "description": "d",
        "made_of": [],
        "provides": [],
        "reuse_policy": "r",
        "status": "s",
    }
    (tier / "c.json").write_text(json.dumps(prefix_bad), encoding="utf-8")

    dir_mismatch = {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": "a1.ok2",
        "tier": "a0_qk_constants",
        "name": "n",
        "kind": "k",
        "description": "d",
        "made_of": [],
        "provides": [],
        "reuse_policy": "r",
        "status": "s",
    }
    (tier / "d.json").write_text(json.dumps(dir_mismatch), encoding="utf-8")

    r = validate_rebuild_v11(root)
    codes = {f.get("code") for f in r["findings"]}
    assert "MISSING_FIELD" in codes
    assert "INVALID_TIER" in codes
    assert "TIER_PREFIX_MISMATCH" in codes
    assert "TIER_DIR_MISMATCH" in codes


def test_validate_rebuild_schema_warn_made_of_not_list_duplicate_id_extra_dir(
    tmp_path: Path,
) -> None:
    root = tmp_path / "out"
    a1 = root / "a1_at_functions"
    a1.mkdir(parents=True)
    (root / "extra_loose_dir").mkdir()

    dup_sidecar = {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": "a1.dup",
        "tier": "a1_at_functions",
        "name": "n",
        "kind": "k",
        "description": "d",
        "made_of": [],
        "provides": [],
        "reuse_policy": "r",
        "status": "s",
    }
    (a1 / "one.json").write_text(json.dumps(dup_sidecar), encoding="utf-8")
    (a1 / "two.json").write_text(json.dumps(dup_sidecar), encoding="utf-8")

    old_schema = {**dup_sidecar, "id": "a1.oldschema", "component_schema": "OLD-SCHEMA"}
    (a1 / "zero.json").write_text(json.dumps(old_schema), encoding="utf-8")

    bad_made = {**dup_sidecar, "id": "a1.other", "made_of": "nope"}
    (a1 / "three.json").write_text(json.dumps(bad_made), encoding="utf-8")

    r = validate_rebuild_v11(root)
    codes = [f.get("code") for f in r["findings"]]
    assert "SCHEMA_VERSION" in codes
    assert "DUPLICATE_ID" in codes
    assert "MADE_OF_NOT_LIST" in codes
    assert "EXTRA_TOP_LEVEL_DIR" in codes
    by_code = r["summary"]["by_code"]
    assert by_code.get("SCHEMA_VERSION", 0) >= 1


def test_materialize_skips_without_body_invalid_tier_or_id(tmp_path: Path) -> None:
    plan = {
        "proposed_components": [
            {"id": "a1.x", "tier": "a1_at_functions", "name": "n", "body": ""},
            {"id": "", "tier": "a1_at_functions", "name": "n", "body": "x=1\n"},
            {"id": "a1.y", "tier": "not_valid", "name": "n", "body": "y=1\n"},
            {"id": "a1.z", "tier": "a1_at_functions", "name": "z", "body": "z=1\n"},
        ],
    }
    r = materialize_gap_plan_to_tree(plan, tmp_path, "t1", write_json_sidecars=False)
    assert r["written_count"] == 1
    assert r["by_tier"].get("a1_at_functions") == 1


def test_repo_stats_non_dir_and_iterdir_oserror(tmp_path: Path) -> None:
    f = tmp_path / "file.txt"
    f.write_text("x", encoding="utf-8")
    surf = compute_repo_surface(f)
    assert surf["total_files"] == 0

    root = tmp_path / "root"
    root.mkdir()

    def boom(*_a: object, **_k: object) -> None:
        raise OSError("denied")

    with patch("pathlib.Path.iterdir", boom):
        assert _walk_top_level_dirs(root) == []


def test_compute_repo_surface_walks_py_files(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.py").write_text("y=1\n", encoding="utf-8")
    surf = compute_repo_surface(tmp_path)
    assert surf["python_files"] == 2
    assert surf["total_files"] == 2
