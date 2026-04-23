#!/usr/bin/env python3
"""ADE strict harness — CNA / MAP preflight for the duplicated swarm under ``ADE/``.

Stdlib only. Used by:

- ``python ADE/harness/ade_hook_gate.py context`` — prints markdown for hook merge.
- ``python ADE/harness/ade_hook_gate.py verify`` — exit 1 on **errors** (warnings alone do not fail).

Environment:

- ``ADE_HARNESS=0`` — skip all checks.
- ``ADE_VERIFY_STRICT=1`` — ``verify`` also treats missing ``cna-seed.yaml`` / ``symbols.txt`` as errors.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ADE_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ADE_ROOT.parent


def _scan() -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    if os.environ.get("ADE_HARNESS", "1").strip() == "0":
        return [], []

    errors: list[str] = []
    warnings: list[str] = []
    strict = os.environ.get("ADE_VERIFY_STRICT", "").strip() == "1"

    rules = WORKSPACE / "RULES.md"
    if not rules.is_file():
        errors.append(f"missing `{rules.as_posix()}` (RULES first-read)")

    for rel in ("_PROTOCOL.md", "ASS_ADE_MONADIC_CODING.md"):
        if not (ADE_ROOT / rel).is_file():
            errors.append(f"missing `ADE/{rel}`")

    seeds = [
        WORKSPACE / "ass-ade-v1.1" / ".ass-ade" / "specs" / "cna-seed.yaml",
        WORKSPACE / "ass-ade" / ".ass-ade" / "specs" / "cna-seed.yaml",
    ]
    if not any(p.is_file() for p in seeds):
        msg = "missing `cna-seed.yaml` (CNA grammar seed — add under v1.1 or legacy `ass-ade` specs)"
        (errors if strict else warnings).append(msg)

    symbols = WORKSPACE / "scripts" / "leak_patterns" / "symbols.txt"
    if not symbols.is_file():
        msg = "missing `scripts/leak_patterns/symbols.txt` (CNA sovereign blocklist)"
        (errors if strict else warnings).append(msg)

    chk = ADE_ROOT / "check_swarm_prompt_alignment.py"
    if chk.is_file():
        r = subprocess.run(
            [sys.executable, str(chk)],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=90,
        )
        if r.returncode != 0:
            tail = (r.stderr or r.stdout or "").strip()[:1600]
            msg = "`python ADE/check_swarm_prompt_alignment.py` failed"
            if tail:
                msg = f"{msg}: {tail[:800]}"
            errors.append(msg)

    if not (ADE_ROOT / "25-ade-harness-sentinel.prompt.md").is_file():
        errors.append("missing `ADE/25-ade-harness-sentinel.prompt.md` (harness sentinel)")

    return errors, warnings


def _markdown(errors: list[str], warnings: list[str]) -> str:
    if not errors and not warnings:
        return ""
    lines: list[str] = ["### [ADE STRICT HARNESS]", ""]
    if errors:
        lines.append("**Errors (resolve before MAP-complete claims):**")
        lines.extend(f"- {e}" for e in errors)
        lines.append("")
    if warnings:
        lines.append("**Warnings (CNA completeness):**")
        lines.extend(f"- {w}" for w in warnings)
        lines.append("")
    lines.extend(
        [
            "Commands: `python ADE/sync_ade_swarm_to_cursor.py` · "
            "`python ADE/harness/verify_ade_harness.py` · "
            "skill `ade-harness`.",
        ]
    )
    return "\n".join(lines)


def cmd_context() -> int:
    err, warn = _scan()
    md = _markdown(err, warn)
    if md:
        print(md)
    return 0


def cmd_verify() -> int:
    err, warn = _scan()
    if err:
        print(_markdown(err, warn), file=sys.stderr)
        return 1
    if warn:
        print("\n".join(f"[ADE warn] {w}" for w in warn))
    print("ADE harness verify: OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="ade_hook_gate")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("context", help="print markdown block for hook merge (stdout)")
    sub.add_parser("verify", help="exit 1 on harness errors (see ADE_VERIFY_STRICT)")
    args = p.parse_args()
    if args.cmd == "context":
        return cmd_context()
    if args.cmd == "verify":
        return cmd_verify()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
