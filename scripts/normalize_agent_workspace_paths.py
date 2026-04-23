#!/usr/bin/env python3
"""Replace hard-coded C:\\!atomadic\\ paths in agents/ with ATOMADIC_WORKSPACE/.

Run from repo root:
  python scripts/normalize_agent_workspace_paths.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("c:\\\\!atomadic\\\\", "<ATOMADIC_WORKSPACE>/"),
    ("C:\\\\!atomadic\\\\", "<ATOMADIC_WORKSPACE>/"),
    ("c:\\!atomadic\\", "<ATOMADIC_WORKSPACE>/"),
    ("C:\\!atomadic\\", "<ATOMADIC_WORKSPACE>/"),
    ("c:/!atomadic/", "<ATOMADIC_WORKSPACE>/"),
    ("C:/!atomadic/", "<ATOMADIC_WORKSPACE>/"),
)

# Only prose + registry — Python under agents/ may need Path(__file__) logic instead.
SUFFIXES = {".md", ".json", ".yaml", ".yml"}


def _fix_mixed_separators(text: str) -> str:
    """Normalize accidental `\\` segments after drive → placeholder replacement."""
    new = text
    for old, rep in (
        ("<ATOMADIC_WORKSPACE>/agents\\", "<ATOMADIC_WORKSPACE>/agents/"),
        ("<ATOMADIC_WORKSPACE>/ass-ade\\", "<ATOMADIC_WORKSPACE>/ass-ade/"),
        # `ass-ade\.ass-ade\` from Windows paths
        ("<ATOMADIC_WORKSPACE>/ass-ade\\.", "<ATOMADIC_WORKSPACE>/ass-ade/."),
        ("<ATOMADIC_WORKSPACE>/.ato-plans\\", "<ATOMADIC_WORKSPACE>/.ato-plans/"),
        ("<ATOMADIC_WORKSPACE>/!atomadic-private\\", "<ATOMADIC_WORKSPACE>/!atomadic-private/"),
    ):
        new = new.replace(old, rep)

    def _slash_backticks(m: re.Match[str]) -> str:
        inner = m.group(1).replace("\\", "/")
        return f"`{inner}`"

    new = re.sub(r"`(<ATOMADIC_WORKSPACE>[^`]+)`", _slash_backticks, new)
    return new


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    agents = root / "agents"
    if not agents.is_dir():
        print("agents/ not found", file=sys.stderr)
        return 1
    changed = 0
    for path in agents.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for old, rep in REPLACEMENTS:
            new = new.replace(old, rep)
        new = _fix_mixed_separators(new)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
            print("updated:", path.relative_to(root))
    print(f"done, files changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
