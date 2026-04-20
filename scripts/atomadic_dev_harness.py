#!/usr/bin/env python3
"""Local dev harness — chain evolution-context check and pytest (stdio only, no MCP)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run(cmd: list[str], *, cwd: Path) -> int:
    print("+ " + " ".join(cmd), file=sys.stderr)
    return subprocess.call(cmd, cwd=str(cwd), env=os.environ.copy())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run check_evolution_context + a narrow pytest slice (default).",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run check_evolution_context + full tests/ (same as CI python-tests).",
    )
    parser.add_argument(
        "--evolution-only",
        action="store_true",
        help="Only run scripts/check_evolution_context.py against the roadmap.",
    )
    args = parser.parse_args(argv)
    root = _repo_root()
    py = sys.executable
    evo = [
        py,
        str(root / "scripts" / "check_evolution_context.py"),
        "--roadmap",
        str(root / ".ass-ade" / "ass-ade-suite-roadmap.json"),
    ]
    rc = _run(evo, cwd=root)
    if rc != 0:
        return rc
    if args.evolution_only:
        return 0

    if args.full:
        tests = [py, "-m", "pytest", "tests/", "-q", "--tb=line"]
    else:
        tests = [
            py,
            "-m",
            "pytest",
            "tests/test_check_evolution_context.py",
            "tests/test_mcp_manifest_parity.py",
            "tests/test_demos_and_import_budget.py",
            "-q",
            "--tb=short",
        ]
    return _run(tests, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
