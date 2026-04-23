#!/usr/bin/env python3
"""Verify pipeline *.prompt.md files include mandatory Atomadic protocol anchors.

Run from repo root:

  python agents/check_swarm_prompt_alignment.py

Exit 1 if any required substring is missing. Used in CI (ass-ade-ship) and locally
after bulk prompt edits.
"""

from __future__ import annotations

import sys
from pathlib import Path

AGENTS = Path(__file__).resolve().parent

REQUIRED_SUBSTRINGS: tuple[tuple[str, str], ...] = (
    ("## Protocol", "section header"),
    ("_PROTOCOL.md", "protocol file reference"),
    ("MAP = TERRAIN", "Axiom 1 anchor (spelling as in prompts)"),
    ("ATOMADIC_WORKSPACE", "path placeholder"),
)


def main() -> int:
    prompts = sorted(AGENTS.glob("[0-9][0-9]-*.prompt.md"))
    if not prompts:
        print("No pipeline *.prompt.md files found.", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in prompts:
        text = path.read_text(encoding="utf-8")
        for needle, desc in REQUIRED_SUBSTRINGS:
            if needle not in text:
                failures.append(f"{path.name}: missing {desc} ({needle!r})")

    if failures:
        print("Swarm prompt alignment check FAILED:\n", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"OK: {len(prompts)} pipeline prompts include protocol anchors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
