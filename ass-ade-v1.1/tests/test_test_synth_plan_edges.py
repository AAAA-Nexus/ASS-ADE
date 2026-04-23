from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade_v11.a1_at_functions.test_synth_plan import (
    load_manifest_qualnames,
    manifest_drift,
    qualname_for_src_py,
)


def test_manifest_drift_when_content_drifted(repo_root: Path) -> None:
    man = repo_root / "tests" / "generated_smoke" / "_qualnames.json"
    original = man.read_text(encoding="utf-8")
    try:
        man.write_text('["bogus.import.only"]\n', encoding="utf-8")
        d = manifest_drift(repo_root)
        assert d["ok"] is False
        assert d["reason"] == "drift"
        assert d["current"] == ["bogus.import.only"]
    finally:
        man.write_text(original, encoding="utf-8")


def test_manifest_drift_when_manifest_missing(repo_root: Path, tmp_path: Path) -> None:
    man = repo_root / "tests" / "generated_smoke" / "_qualnames.json"
    assert man.is_file()
    backup = tmp_path / "_qualnames.bak"
    man.rename(backup)
    try:
        d = manifest_drift(repo_root)
        assert d["ok"] is False
        assert d["reason"] == "missing_file"
    finally:
        backup.rename(man)


def test_load_manifest_invalid_json(tmp_path: Path) -> None:
    d = tmp_path / "tests" / "generated_smoke"
    d.mkdir(parents=True)
    (d / "_qualnames.json").write_text("not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_manifest_qualnames(tmp_path)


def test_load_manifest_not_a_list(tmp_path: Path) -> None:
    d = tmp_path / "tests" / "generated_smoke"
    d.mkdir(parents=True)
    (d / "_qualnames.json").write_text('{"x": 1}', encoding="utf-8")
    with pytest.raises(ValueError, match="manifest must"):
        load_manifest_qualnames(tmp_path)


def test_qualname_nested_module(repo_root: Path) -> None:
    p = repo_root / "src" / "ass_ade_v11" / "a1_at_functions" / "gap_fill.py"
    assert qualname_for_src_py(p, repo_root) == "ass_ade_v11.a1_at_functions.gap_fill"
