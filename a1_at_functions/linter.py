from __future__ import annotations

"""Local codebase lint runner for the ass-ade lint command.

Runs language-appropriate linters. Returns structured findings
that the CLI layer can display or forward to the Nexus API.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ass_ade.local.repo import DEFAULT_IGNORED_DIRS


def detect_linters(root: Path) -> list[str]:
    found: list[str] = []

    pyproject = root / "pyproject.toml"
    pyproject_raw = ""
    if pyproject.exists():
        try:
            pyproject_raw = pyproject.read_text(encoding="utf-8")
        except Exception:
            pass

    ruff_toml = root / "ruff.toml"
    if (pyproject_raw and "[tool.ruff]" in pyproject_raw) or ruff_toml.exists():
        if shutil.which("ruff"):
            found.append("ruff")

    mypy_ini = root / "mypy.ini"
    if mypy_ini.exists() or (pyproject_raw and "[tool.mypy]" in pyproject_raw):
        if shutil.which("mypy"):
            found.append("mypy")

    if pyproject_raw and "[tool.pyright]" in pyproject_raw:
        if shutil.which("pyright"):
            found.append("pyright")

    for name in (
        ".eslintrc",
        ".eslintrc.js",
        ".eslintrc.cjs",
        ".eslintrc.mjs",
        ".eslintrc.json",
        ".eslintrc.yaml",
        ".eslintrc.yml",
    ):
        if (root / name).exists():
            if shutil.which("eslint"):
                found.append("eslint")
            break

    for name in (
        ".prettierrc",
        ".prettierrc.js",
        ".prettierrc.cjs",
        ".prettierrc.mjs",
        ".prettierrc.json",
        ".prettierrc.yaml",
        ".prettierrc.yml",
        ".prettierrc.toml",
        "prettier.config.js",
        "prettier.config.cjs",
    ):
        if (root / name).exists():
            if shutil.which("prettier"):
                found.append("prettier")
            break

    if (root / "Cargo.toml").exists() and shutil.which("cargo"):
        found.append("clippy")

    if (root / "go.mod").exists() and shutil.which("go"):
        found.append("go-vet")

    return found


def run_ruff(root: Path, fix: bool = False) -> dict[str, Any]:
    if not shutil.which("ruff"):
        return {"linter": "ruff", "ok": None, "error": "ruff not found"}

    cmd = [
        "ruff", "check", str(root), "--output-format", "json",
        "--exclude", ".pytest_tmp",
    ]
    if fix:
        cmd.append("--fix")

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        # Use stdout only for JSON — stderr is ruff's error/status channel.
        raw = proc.stdout or ""
        if not raw.strip():
            # ruff produced no JSON output; treat as environment error, not a lint failure
            err = proc.stderr.strip() or "ruff produced no output"
            return {
                "linter": "ruff", "ok": None, "error": err,
                "findings": [], "error_count": 0, "warning_count": 0,
            }
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "linter": "ruff", "ok": None, "raw": raw, "error": "failed to parse output",
                "findings": [], "error_count": 0, "warning_count": 0,
            }

        findings: list[dict[str, Any]] = []
        error_count = 0
        warning_count = 0

        for item in data:
            code: str = item.get("code") or ""
            location = item.get("location") or {}
            finding = {
                "file": item.get("filename", ""),
                "row": location.get("row", 0),
                "col": location.get("column", 0),
                "code": code,
                "message": item.get("message", ""),
            }
            findings.append(finding)
            # E/F codes are errors; W codes are warnings
            if code.startswith("W"):
                warning_count += 1
            else:
                error_count += 1

        return {
            "linter": "ruff",
            "ok": len(findings) == 0,
            "error_count": error_count,
            "warning_count": warning_count,
            "findings": findings,
            "raw": raw,
        }
    except subprocess.TimeoutExpired:
        return {"linter": "ruff", "ok": None, "error": "timed out"}
    except Exception as exc:
        return {"linter": "ruff", "ok": None, "error": str(exc)}


def run_pyright(root: Path) -> dict[str, Any]:
    if not shutil.which("pyright"):
        return {"linter": "pyright", "ok": None, "error": "pyright not found"}

    cmd = ["pyright", "--outputjson", str(root)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
        raw = proc.stdout or proc.stderr or ""
        try:
            data = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            return {"linter": "pyright", "ok": False, "raw": raw, "error": "failed to parse output"}

        general_diag = data.get("generalDiagnostics") or []
        findings: list[dict[str, Any]] = []
        error_count = 0
        warning_count = 0

        for item in general_diag:
            severity = item.get("severity", "error")
            finding = {
                "file": item.get("file", ""),
                "row": (item.get("range") or {}).get("start", {}).get("line", 0),
                "col": (item.get("range") or {}).get("start", {}).get("character", 0),
                "code": item.get("rule", ""),
                "message": item.get("message", ""),
            }
            findings.append(finding)
            if severity == "warning":
                warning_count += 1
            elif severity == "error":
                error_count += 1

        summary = data.get("summary") or {}
        ok = summary.get("errorCount", error_count) == 0

        return {
            "linter": "pyright",
            "ok": ok,
            "error_count": error_count,
            "warning_count": warning_count,
            "findings": findings,
            "raw": raw,
        }
    except subprocess.TimeoutExpired:
        return {"linter": "pyright", "ok": None, "error": "timed out"}
    except Exception as exc:
        return {"linter": "pyright", "ok": None, "error": str(exc)}


def _run_generic(linter: str, cmd: list[str], timeout: int = 60) -> dict[str, Any]:
    """Run a linter command and return a minimal result dict."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        raw = proc.stdout + proc.stderr
        ok = proc.returncode == 0
        return {"linter": linter, "ok": ok, "findings": [], "raw": raw}
    except subprocess.TimeoutExpired:
        return {"linter": linter, "ok": None, "error": "timed out"}
    except Exception as exc:
        return {"linter": linter, "ok": None, "error": str(exc)}


def run_linters(root: Path, fix: bool = False) -> dict[str, Any]:
    linters = detect_linters(root)
    results: dict[str, Any] = {}

    for linter in linters:
        if linter == "ruff":
            results["ruff"] = run_ruff(root, fix=fix)
        elif linter == "pyright":
            results["pyright"] = run_pyright(root)
        elif linter == "mypy":
            results["mypy"] = _run_generic("mypy", ["mypy", str(root)])
        elif linter == "eslint":
            cmd = ["eslint", str(root), "--format", "json"]
            results["eslint"] = _run_generic("eslint", cmd)
        elif linter == "prettier":
            cmd = ["prettier", "--check", str(root)]
            results["prettier"] = _run_generic("prettier", cmd)
        elif linter == "clippy":
            cmd = ["cargo", "clippy", "--manifest-path", str(root / "Cargo.toml")]
            results["clippy"] = _run_generic("clippy", cmd, timeout=120)
        elif linter == "go-vet":
            cmd = ["go", "vet", "./..."]
            results["go-vet"] = _run_generic("go-vet", cmd)

    total_findings = sum(
        len(r.get("findings") or []) for r in results.values()
    )
    overall_ok = bool(linters) and all(
        r.get("ok") is True for r in results.values()
    )

    return {
        "root": str(root.resolve()),
        "linters_run": list(results.keys()),
        "results": results,
        "overall_ok": overall_ok,
        "total_findings": total_findings,
    }
