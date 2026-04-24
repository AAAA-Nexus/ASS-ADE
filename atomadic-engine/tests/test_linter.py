from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.local.linter import detect_linters, run_linters, run_ruff


# ---------------------------------------------------------------------------
# detect_linters
# ---------------------------------------------------------------------------


def test_detect_linters_python_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[tool.ruff]\nline-length = 88\n",
        encoding="utf-8",
    )

    # Ensure shutil.which("ruff") returns a truthy value so the linter is detected
    with patch("ass_ade.local.linter.shutil.which", side_effect=lambda cmd: cmd if cmd == "ruff" else None):
        result = detect_linters(tmp_path)

    assert "ruff" in result


def test_detect_linters_empty_dir(tmp_path: Path) -> None:
    result = detect_linters(tmp_path)

    assert isinstance(result, list)
    # No crash expected even with empty directory


# ---------------------------------------------------------------------------
# run_ruff
# ---------------------------------------------------------------------------


def test_run_ruff_not_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Make shutil.which return None so run_ruff takes the early-exit path
    monkeypatch.setattr("ass_ade.local.linter.shutil.which", lambda _cmd: None)

    result = run_ruff(tmp_path)

    assert result.get("ok") is None
    assert "ruff not found" in result.get("error", "")


# ---------------------------------------------------------------------------
# run_linters
# ---------------------------------------------------------------------------


def test_run_linters_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "hello.py").write_text("x = 1\n", encoding="utf-8")

    result = run_linters(tmp_path)

    assert isinstance(result, dict)
    assert "root" in result
    assert "linters_run" in result
    assert "results" in result


def test_run_linters_overall_ok_false_on_findings(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
    (tmp_path / "bad.py").write_text("import os\n", encoding="utf-8")

    ruff_with_findings = {
        "linter": "ruff",
        "ok": False,
        "error_count": 5,
        "warning_count": 0,
        "findings": [{"file": "bad.py", "row": 1, "col": 1, "code": "F401", "message": "unused"}] * 5,
        "raw": "[]",
    }

    with (
        patch("ass_ade.local.linter.shutil.which", side_effect=lambda cmd: cmd if cmd == "ruff" else None),
        patch("ass_ade.local.linter.run_ruff", return_value=ruff_with_findings),
    ):
        result = run_linters(tmp_path)

    assert result["overall_ok"] is False
