"""Smoke-test ``tools/assimilate_v11_plus_legacy.py`` (dual-root, no env required)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _repo() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_tool(tmp_path: Path, *, stop_after: str = "gapfill") -> subprocess.CompletedProcess[str]:
    repo = _repo()
    primary = repo / "tests" / "fixtures" / "minimal_pkg"
    legacy = repo / "tests" / "fixtures" / "a1_only"
    script = repo / "tools" / "assimilate_v11_plus_legacy.py"
    book_path = tmp_path / "book.json"
    return subprocess.run(
        [
            sys.executable,
            str(script),
            "-o",
            str(tmp_path),
            "--primary",
            str(primary),
            "--legacy",
            str(legacy),
            "--stop-after",
            stop_after,
            "--rebuild-tag",
            "tool-smoke",
            "--json-out",
            str(book_path),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )


def test_assimilate_tool_gapfill_ok(tmp_path: Path) -> None:
    proc = _run_tool(tmp_path, stop_after="gapfill")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    book = json.loads((tmp_path / "book.json").read_text(encoding="utf-8"))
    p0 = book.get("phase0") or {}
    p2 = book.get("phase2") or {}
    assert p0.get("verdict") == "READY_FOR_PHASE_1"
    assert len(p0.get("source_roots") or []) == 2
    assert len((p2.get("gap_plan") or {}).get("proposed_components") or []) >= 1
