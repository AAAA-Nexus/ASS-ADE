#!/usr/bin/env python3
"""Strict ADE harness gate for CI and pre-push (exit non-zero on any failure)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    gate = ROOT / "harness" / "ade_hook_gate.py"
    r = subprocess.run([sys.executable, str(gate), "verify"], cwd=str(ROOT.parent))
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
