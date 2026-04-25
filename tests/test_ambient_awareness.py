"""Tests for a2_mo_composites/ambient_awareness.py."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.a2_mo_composites.ambient_awareness import AmbientAwareness, _find_repo_root


# ── factory ────────────────────────────────────────────────────────────────────


def test_from_cwd_returns_ambient_awareness():
    aw = AmbientAwareness.from_cwd()
    assert isinstance(aw, AmbientAwareness)
    assert isinstance(aw.repo_root, Path)


def test_default_repo_root_is_path(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    assert aw.repo_root == tmp_path


# ── overnight_commits ──────────────────────────────────────────────────────────


def test_overnight_commits_returns_list_on_success(tmp_path):
    fake_output = "abc1234 fix: stabilise boot sequence\ndef5678 feat: add wake page\n"
    with patch("ass_ade.a2_mo_composites.ambient_awareness.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=fake_output)
        aw = AmbientAwareness(repo_root=tmp_path)
        result = aw.overnight_commits()
    assert result == ["abc1234 fix: stabilise boot sequence", "def5678 feat: add wake page"]


def test_overnight_commits_returns_empty_on_git_failure(tmp_path):
    with patch("ass_ade.a2_mo_composites.ambient_awareness.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        aw = AmbientAwareness(repo_root=tmp_path)
        assert aw.overnight_commits() == []


def test_overnight_commits_returns_empty_on_exception(tmp_path):
    with patch(
        "ass_ade.a2_mo_composites.ambient_awareness.subprocess.run",
        side_effect=FileNotFoundError("git not found"),
    ):
        aw = AmbientAwareness(repo_root=tmp_path)
        assert aw.overnight_commits() == []


def test_overnight_commits_strips_blank_lines(tmp_path):
    fake_output = "\nabc1234 commit one\n\ndef5678 commit two\n\n"
    with patch("ass_ade.a2_mo_composites.ambient_awareness.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=fake_output)
        aw = AmbientAwareness(repo_root=tmp_path)
        result = aw.overnight_commits()
    assert "" not in result
    assert len(result) == 2


# ── last_test_status ───────────────────────────────────────────────────────────


def test_last_test_status_returns_none_when_cache_missing(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    assert aw.last_test_status() is None


def test_last_test_status_reads_cache_file(tmp_path):
    cache_dir = tmp_path / ".ass-ade"
    cache_dir.mkdir()
    cache_file = cache_dir / "last_test_run.json"
    cache_file.write_text(
        json.dumps({"passed": 501, "failed": 0, "ts": "2026-04-24T06:00:00Z"}),
        encoding="utf-8",
    )
    aw = AmbientAwareness(repo_root=tmp_path)
    status = aw.last_test_status()
    assert status is not None
    assert "501" in status
    assert "0 failed" in status


def test_last_test_status_returns_none_on_corrupt_json(tmp_path):
    cache_dir = tmp_path / ".ass-ade"
    cache_dir.mkdir()
    (cache_dir / "last_test_run.json").write_text("not json", encoding="utf-8")
    aw = AmbientAwareness(repo_root=tmp_path)
    assert aw.last_test_status() is None


# ── inference_health ───────────────────────────────────────────────────────────


def test_inference_health_returns_none_when_no_env(tmp_path, monkeypatch):
    monkeypatch.delenv("ATOMADIC_INFERENCE_URL", raising=False)
    aw = AmbientAwareness(repo_root=tmp_path)
    assert aw.inference_health() is None


def test_inference_health_returns_true_on_healthy_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("ATOMADIC_INFERENCE_URL", "http://localhost:9999")

    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.status = 200

    with patch("ass_ade.a2_mo_composites.ambient_awareness.urllib.request.urlopen", return_value=mock_resp):
        aw = AmbientAwareness(repo_root=tmp_path)
        assert aw.inference_health() is True


def test_inference_health_returns_false_on_connection_error(tmp_path, monkeypatch):
    monkeypatch.setenv("ATOMADIC_INFERENCE_URL", "http://localhost:9999")
    with patch(
        "ass_ade.a2_mo_composites.ambient_awareness.urllib.request.urlopen",
        side_effect=OSError("refused"),
    ):
        aw = AmbientAwareness(repo_root=tmp_path)
        assert aw.inference_health() is False


# ── should_greet ───────────────────────────────────────────────────────────────


def test_should_greet_true_when_morning_and_no_commits(tmp_path, monkeypatch):
    with patch("ass_ade.a2_mo_composites.ambient_awareness.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2026, 4, 24, 7, 0, 0, tzinfo=timezone.utc)
        aw = AmbientAwareness(repo_root=tmp_path)
        with patch.object(aw, "overnight_commits", return_value=[]):
            # In morning window: should greet
            assert aw.should_greet() is True


def test_should_greet_true_when_commits_exist_outside_morning(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    with patch.object(aw, "overnight_commits", return_value=["abc1234 some work"]):
        # has_work is True, so should greet regardless of hour
        assert aw.should_greet() is True


def test_should_greet_false_when_no_commits_and_outside_morning(tmp_path):
    with patch("ass_ade.a2_mo_composites.ambient_awareness.datetime") as mock_dt:
        # 2am UTC — before morning window
        mock_dt.now.return_value = datetime(2026, 4, 24, 2, 0, 0, tzinfo=timezone.utc)
        aw = AmbientAwareness(repo_root=tmp_path)
        with patch.object(aw, "overnight_commits", return_value=[]):
            assert aw.should_greet() is False


# ── generate_status_report ─────────────────────────────────────────────────────


def test_generate_status_report_contains_expected_sections(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    with (
        patch.object(aw, "overnight_commits", return_value=["abc1234 fix: something"]),
        patch.object(aw, "last_test_status", return_value="501 passed, 0 failed (at 2026-04-24)"),
        patch.object(aw, "inference_health", return_value=None),
    ):
        report = aw.generate_status_report()
    assert "overnight report" in report.lower()
    assert "1 commit" in report
    assert "abc1234" in report
    assert "501 passed" in report
    assert "not configured" in report


def test_generate_status_report_caches_result(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    call_count = []

    def counting_commits():
        call_count.append(1)
        return []

    with (
        patch.object(aw, "overnight_commits", side_effect=counting_commits),
        patch.object(aw, "last_test_status", return_value=None),
        patch.object(aw, "inference_health", return_value=None),
    ):
        r1 = aw.generate_status_report()
        r2 = aw.generate_status_report()

    assert r1 is r2
    assert len(call_count) == 1  # called only once


def test_generate_status_report_no_commits_message(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    with (
        patch.object(aw, "overnight_commits", return_value=[]),
        patch.object(aw, "last_test_status", return_value=None),
        patch.object(aw, "inference_health", return_value=None),
    ):
        report = aw.generate_status_report()
    assert "No commits overnight" in report


# ── as_wake_data ───────────────────────────────────────────────────────────────


def test_as_wake_data_shape(tmp_path):
    aw = AmbientAwareness(repo_root=tmp_path)
    with (
        patch.object(aw, "overnight_commits", return_value=["abc fix", "def feat"]),
        patch.object(aw, "last_test_status", return_value="501 passed, 0 failed (at T)"),
        patch.object(aw, "inference_health", return_value=True),
    ):
        data = aw.as_wake_data()
    assert data["commits"] == 2
    assert data["healthy"] is True
    assert "tests" in data
    assert "tests_label" in data


# ── _find_repo_root ────────────────────────────────────────────────────────────


def test_find_repo_root_finds_git_dir(tmp_path):
    (tmp_path / ".git").mkdir()
    subdir = tmp_path / "a" / "b"
    subdir.mkdir(parents=True)
    import os
    old = os.getcwd()
    try:
        os.chdir(subdir)
        root = _find_repo_root()
        assert root == tmp_path
    finally:
        os.chdir(old)


def test_find_repo_root_falls_back_to_cwd(tmp_path):
    import os
    old = os.getcwd()
    try:
        os.chdir(tmp_path)
        root = _find_repo_root()
        # Without a .git dir anywhere in tmp_path ancestry, it returns cwd
        assert isinstance(root, Path)
    finally:
        os.chdir(old)
