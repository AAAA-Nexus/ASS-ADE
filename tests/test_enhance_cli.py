from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app

runner = CliRunner()

# Detect whether the enhance command is registered at import time so the
# skipif marker can reference it as a module-level constant.
# Use exit_code==0 from `enhance --help` as the authoritative check: if the
# command is not registered Typer returns exit_code 2 (no such command).
_ENHANCE_REGISTERED = runner.invoke(app, ["enhance", "--help"]).exit_code == 0


# ---------------------------------------------------------------------------
# enhance help
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _ENHANCE_REGISTERED,
    reason="enhance command not yet registered",
)
def test_enhance_help() -> None:
    result = runner.invoke(app, ["enhance", "--help"])

    assert result.exit_code == 0
    assert "enhance" in result.output.lower()


# ---------------------------------------------------------------------------
# enhance --local-only (smoke test with bare-except and TODO file)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _ENHANCE_REGISTERED,
    reason="enhance command not yet registered",
)
def test_enhance_local_only(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text(
        "def do_work():\n"
        "    try:\n"
        "        pass\n"
        "    except:\n"
        "        pass\n"
        "    # TODO: fix later\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["enhance", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    assert "findings" in result.output.lower() or "improvement" in result.output.lower()


# ---------------------------------------------------------------------------
# enhance --json --local-only
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _ENHANCE_REGISTERED,
    reason="enhance command not yet registered",
)
def test_enhance_json_output(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("def f():\n    pass  # TODO: implement\n", encoding="utf-8")

    result = runner.invoke(app, ["enhance", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    start = result.output.find("{")
    assert start != -1, f"No JSON in output:\n{result.output}"
    payload = json.loads(result.output[start:], strict=False)
    assert "total_findings" in payload


# ---------------------------------------------------------------------------
# enhance nonexistent path
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _ENHANCE_REGISTERED,
    reason="enhance command not yet registered",
)
def test_enhance_nonexistent_path() -> None:
    result = runner.invoke(app, ["enhance", "/nonexistent/path/xyz"])

    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# enhance --apply with empty IDs
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _ENHANCE_REGISTERED,
    reason="enhance command not yet registered",
)
def test_enhance_apply_requires_ids(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["enhance", str(tmp_path), "--apply", "", "--local-only"])

    # Should exit gracefully — either 0 (skipped/noop) or 1 (validation error).
    # Critically, it must not crash with an unhandled exception.
    assert result.exit_code in (0, 1)
    assert result.exception is None or isinstance(result.exception, SystemExit)
