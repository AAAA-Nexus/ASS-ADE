from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_minimal_project(root: Path) -> None:
    """Write just enough files for docs/lint/certify to have something to process."""
    (root / "pyproject.toml").write_text(
        '[project]\nname = "testpkg"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    (root / "main.py").write_text("def main(): pass\n", encoding="utf-8")


def _extract_json(output: str) -> dict:
    """Extract a JSON object from CLI output.

    Rich may wrap long path strings across lines, inserting a literal newline
    control character inside a JSON string value. Use strict=False to allow
    those embedded control characters while parsing.
    """
    start = output.find("{")
    assert start != -1, f"No JSON '{{' found in output:\n{output}"
    raw = output[start:]
    return json.loads(raw, strict=False)


# ---------------------------------------------------------------------------
# docs command
# ---------------------------------------------------------------------------


def test_docs_local_only(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    # Should report how many docs were written
    assert "docs written" in result.stdout or "written" in result.stdout.lower()


def test_docs_json_output(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "files_generated" in payload


def test_docs_nonexistent_path() -> None:
    result = runner.invoke(app, ["docs", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# lint command
# ---------------------------------------------------------------------------


def test_lint_local_path(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["lint", str(tmp_path), "--json"])

    assert result.exit_code in (0, 1)
    payload = _extract_json(result.stdout)
    assert "linters_run" in payload


def test_lint_nonexistent_path() -> None:
    result = runner.invoke(app, ["lint", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# certify command
# ---------------------------------------------------------------------------


def test_certify_local_only(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    cert_path = tmp_path / "CERTIFICATE.json"
    assert cert_path.exists(), "CERTIFICATE.json was not written"


def test_certify_json_output(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "schema" in payload


def test_certify_nonexistent_path() -> None:
    result = runner.invoke(app, ["certify", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1


def test_certify_version_flag(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(
        app,
        ["certify", str(tmp_path), "--version", "9.9.9", "--local-only"],
    )

    assert result.exit_code == 0
    cert_path = tmp_path / "CERTIFICATE.json"
    assert cert_path.exists()
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert["version"] == "9.9.9"
