"""Namespace conflict detection for multi-source MAP."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from ass_ade.a0_qk_constants.policy_types import RootPolicy
from ass_ade.a1_at_functions.conflict_detector import (
    _file_hash,
    detect_namespace_conflicts,
    format_conflict_report,
)


def test_detect_namespace_conflicts_flags_divergent_stems(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    (a / "utils.py").write_text("x = 1\n", encoding="utf-8")
    (b / "utils.py").write_text("y = 2\n", encoding="utf-8")
    r = detect_namespace_conflicts([a, b])
    assert r["clean"] is False
    assert r["conflict_count"] >= 1
    assert any(c["stem"] == "utils" for c in r["conflicts"])


def test_identical_copy_not_flagged(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    body = "def f():\n    return 1\n"
    (a / "same.py").write_text(body, encoding="utf-8")
    (b / "same.py").write_text(body, encoding="utf-8")
    r = detect_namespace_conflicts([a, b])
    assert r["clean"] is True


def test_format_conflict_report_empty() -> None:
    assert "No module name" in format_conflict_report({"conflicts": []})


def test_file_hash_returns_empty_on_oserror(tmp_path: Path) -> None:
    f = tmp_path / "unreadable.py"
    f.write_text("x = 1\n", encoding="utf-8")
    with patch.object(Path, "read_bytes", side_effect=OSError("denied")):
        assert _file_hash(f) == ""


def test_skips_paths_under_excluded_dirs_like_venv(tmp_path: Path) -> None:
    """Match ingest: do not descend into .venv / .pytest_tmp when scanning for stem clashes."""
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "utils.py").write_text("x = 1\n", encoding="utf-8")
    vdir = a / ".venv" / "lib"
    vdir.mkdir(parents=True)
    (vdir / "utils.py").write_text("z = 9\n", encoding="utf-8")
    (b / "utils.py").write_text("y = 2\n", encoding="utf-8")
    r = detect_namespace_conflicts([a, b])
    assert r["clean"] is False
    assert any(c["stem"] == "utils" for c in r["conflicts"])
    for c in r["conflicts"]:
        for p in c["sources"]:
            assert ".venv" not in p.replace("\\", "/")


def test_policy_forbid_globs_skip_relative_paths(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    noise = a / "docs" / "rebuild-runs" / "x"
    noise.mkdir(parents=True)
    (noise / "utils.py").write_text("z = 9\n", encoding="utf-8")
    (a / "utils.py").write_text("x = 1\n", encoding="utf-8")
    (b / "utils.py").write_text("y = 2\n", encoding="utf-8")
    pol_a: RootPolicy = {
        "role": "map",
        "license_class": "proprietary",
        "forbid_globs": ("docs/rebuild-runs/**", "**/docs/rebuild-runs/**"),
        "allow_globs": None,
        "max_file_bytes": 2_000_000,
        "binary_handling": "track_only",
    }
    r = detect_namespace_conflicts([a, b], policy_by_root={a.resolve(): pol_a})
    assert r["clean"] is False
    for c in r["conflicts"]:
        for p in c["sources"]:
            assert "rebuild-runs" not in p.replace("\\", "/")


def test_skips_test_prefix_stems(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "test_foo.py").write_text("x = 1\n", encoding="utf-8")
    (b / "test_foo.py").write_text("y = 2\n", encoding="utf-8")
    r = detect_namespace_conflicts([a, b])
    assert r["clean"] is True


def test_non_directory_root_skipped(tmp_path: Path) -> None:
    a = tmp_path / "a"
    a.mkdir()
    bogus = tmp_path / "notadir.py"
    bogus.write_text("", encoding="utf-8")
    (a / "only.py").write_text("v = 1\n", encoding="utf-8")
    r = detect_namespace_conflicts([bogus, a])
    assert r["clean"] is True


def test_format_conflict_report_lists_conflicts(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "core.py").write_text("x = 1\n", encoding="utf-8")
    (b / "core.py").write_text("y = 2\n", encoding="utf-8")
    r = detect_namespace_conflicts([a, b])
    text = format_conflict_report(r)
    assert "namespace conflict" in text.lower()
    assert "core" in text
