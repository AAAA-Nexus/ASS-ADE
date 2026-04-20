"""Tests for ass_ade.engine.version_tracker."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.engine.rebuild.version_tracker import (
    INITIAL_VERSION,
    _aggregate_version,
    _public_python_api,
    assign_version,
    bump_version,
    classify_change,
    content_hash,
    load_prev_versions,
    write_project_version_file,
    write_tier_version_file,
)


# ── bump_version ──────────────────────────────────────────────────────────────

class TestBumpVersion:
    def test_patch(self):
        assert bump_version("0.1.3", "patch") == "0.1.4"

    def test_minor(self):
        assert bump_version("0.1.3", "minor") == "0.2.0"

    def test_major(self):
        assert bump_version("0.1.3", "major") == "1.0.0"

    def test_invalid_falls_back_to_initial(self):
        assert bump_version("not-semver", "patch") == INITIAL_VERSION

    def test_minor_resets_patch(self):
        assert bump_version("1.2.9", "minor") == "1.3.0"

    def test_major_resets_minor_and_patch(self):
        assert bump_version("2.5.7", "major") == "3.0.0"


# ── content_hash ──────────────────────────────────────────────────────────────

class TestContentHash:
    def test_deterministic(self):
        assert content_hash("hello world") == content_hash("hello world")

    def test_different_content(self):
        assert content_hash("foo") != content_hash("bar")

    def test_trailing_whitespace_normalised(self):
        assert content_hash("a  \nb  \n") == content_hash("a\nb")

    def test_returns_16_hex_chars(self):
        h = content_hash("test")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_empty_string(self):
        h = content_hash("")
        assert len(h) == 16


# ── _public_python_api ────────────────────────────────────────────────────────

class TestPublicPythonApi:
    def test_extracts_functions(self):
        body = "def foo(): pass\ndef _bar(): pass\ndef baz(): pass"
        assert _public_python_api(body) == {"foo", "baz"}

    def test_extracts_classes(self):
        body = "class Foo: pass\nclass _Hidden: pass"
        assert _public_python_api(body) == {"Foo"}

    def test_empty_body(self):
        assert _public_python_api("") == set()

    def test_syntax_error_returns_empty(self):
        assert _public_python_api("def (broken") == set()


# ── classify_change ───────────────────────────────────────────────────────────

class TestClassifyChange:
    def test_identical(self):
        body = "def foo(): pass"
        assert classify_change(body, body) == "none"

    def test_patch_internal_change(self):
        old = "def foo():\n    return 1"
        new = "def foo():\n    return 2"
        assert classify_change(old, new) == "patch"

    def test_minor_new_function(self):
        old = "def foo(): pass"
        new = "def foo(): pass\ndef bar(): pass"
        assert classify_change(old, new) == "minor"

    def test_major_removed_function(self):
        old = "def foo(): pass\ndef bar(): pass"
        new = "def foo(): pass"
        assert classify_change(old, new) == "major"

    def test_non_python_falls_back_to_patch(self):
        assert classify_change("old code", "new code", language="rust") == "patch"

    def test_empty_old_body(self):
        new = "def foo(): pass"
        result = classify_change("", new)
        assert result in {"minor", "patch"}


# ── assign_version ────────────────────────────────────────────────────────────

class TestAssignVersion:
    def test_new_artifact(self):
        version, change_type = assign_version("at.foo", "", "python", {})
        assert version == INITIAL_VERSION
        assert change_type == "new"

    def test_unchanged_artifact(self):
        body = "def foo(): pass"
        prev = {
            "at.foo": {
                "version": "0.2.1",
                "body_hash": content_hash(body),
                "body": body,
            }
        }
        version, change_type = assign_version("at.foo", body, "python", prev)
        assert version == "0.2.1"
        assert change_type == "none"

    def test_patch_bump(self):
        old_body = "def foo():\n    return 1"
        new_body = "def foo():\n    return 2"
        prev = {
            "at.foo": {
                "version": "0.1.3",
                "body_hash": content_hash(old_body),
                "body": old_body,
            }
        }
        version, change_type = assign_version("at.foo", new_body, "python", prev)
        assert version == "0.1.4"
        assert change_type == "patch"

    def test_minor_bump(self):
        old_body = "def foo(): pass"
        new_body = "def foo(): pass\ndef bar(): pass"
        prev = {
            "at.foo": {
                "version": "0.1.3",
                "body_hash": content_hash(old_body),
                "body": old_body,
            }
        }
        version, change_type = assign_version("at.foo", new_body, "python", prev)
        assert version == "0.2.0"
        assert change_type == "minor"

    def test_major_bump(self):
        old_body = "def foo(): pass\ndef bar(): pass"
        new_body = "def foo(): pass"
        prev = {
            "at.foo": {
                "version": "0.1.3",
                "body_hash": content_hash(old_body),
                "body": old_body,
            }
        }
        version, change_type = assign_version("at.foo", new_body, "python", prev)
        assert version == "1.0.0"
        assert change_type == "major"


# ── _aggregate_version ────────────────────────────────────────────────────────

class TestAggregateVersion:
    def test_picks_highest(self):
        assert _aggregate_version(["0.1.0", "0.2.0", "0.1.5"]) == "0.2.0"

    def test_empty_list_returns_initial(self):
        assert _aggregate_version([]) == INITIAL_VERSION

    def test_single(self):
        assert _aggregate_version(["1.3.7"]) == "1.3.7"

    def test_major_wins(self):
        assert _aggregate_version(["0.9.9", "1.0.0", "0.9.8"]) == "1.0.0"


# ── load_prev_versions ────────────────────────────────────────────────────────

class TestLoadPrevVersions:
    def test_none_path_returns_empty(self):
        assert load_prev_versions(None) == {}

    def test_nonexistent_path_returns_empty(self, tmp_path: Path):
        assert load_prev_versions(tmp_path / "nope.json") == {}

    def test_loads_from_manifest(self, tmp_path: Path):
        manifest = {
            "components": [
                {
                    "id": "at.foo",
                    "version": "0.2.1",
                    "body_hash": "abc123",
                    "body": "def foo(): pass",
                }
            ]
        }
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        result = load_prev_versions(p)
        assert "at.foo" in result
        assert result["at.foo"]["version"] == "0.2.1"
        assert result["at.foo"]["body_hash"] == "abc123"

    def test_missing_id_skipped(self, tmp_path: Path):
        manifest = {"components": [{"version": "0.1.0"}]}
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        assert load_prev_versions(p) == {}

    def test_invalid_json_returns_empty(self, tmp_path: Path):
        p = tmp_path / "MANIFEST.json"
        p.write_text("not json", encoding="utf-8")
        assert load_prev_versions(p) == {}


# ── write_tier_version_file ───────────────────────────────────────────────────

class TestWriteTierVersionFile:
    def test_writes_file(self, tmp_path: Path):
        tier_dir = tmp_path / "a1_at_functions"
        tier_dir.mkdir()
        modules = [
            {"id": "at.foo", "name": "foo", "version": "0.1.0", "change_type": "new"},
            {"id": "at.bar", "name": "bar", "version": "0.2.0", "change_type": "minor"},
        ]
        path = write_tier_version_file(tier_dir, "a1_at_functions", modules)
        assert Path(path).exists()
        data = json.loads(Path(path).read_text())
        assert data["tier"] == "a1_at_functions"
        assert data["tier_version"] == "0.2.0"
        assert data["module_count"] == 2

    def test_aggregate_version_is_max(self, tmp_path: Path):
        tier_dir = tmp_path / "a2_mo_composites"
        tier_dir.mkdir()
        modules = [
            {"id": "mo.x", "name": "x", "version": "1.0.0", "change_type": "major"},
            {"id": "mo.y", "name": "y", "version": "0.5.0", "change_type": "minor"},
        ]
        path = write_tier_version_file(tier_dir, "a2_mo_composites", modules)
        data = json.loads(Path(path).read_text())
        assert data["tier_version"] == "1.0.0"


# ── write_project_version_file ────────────────────────────────────────────────

class TestWriteProjectVersionFile:
    def test_writes_version_file(self, tmp_path: Path):
        tier_versions = {
            "a0_qk_constants": "0.1.0",
            "a1_at_functions": "0.2.3",
        }
        path = write_project_version_file(tmp_path, tier_versions, "20260418_120000")
        assert Path(path).name == "VERSION"
        lines = Path(path).read_text().splitlines()
        assert lines[0] == "0.2.3"
        assert "rebuild_tag=20260418_120000" in lines

    def test_empty_tiers_returns_initial(self, tmp_path: Path):
        path = write_project_version_file(tmp_path, {}, "tag1")
        first_line = Path(path).read_text().splitlines()[0]
        assert first_line == INITIAL_VERSION
