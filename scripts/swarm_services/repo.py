from __future__ import annotations

import os
from pathlib import Path


def discover_repo_root(explicit: Path | None) -> Path:
    """Return repo root containing ``agents/INDEX.md`` (Atomadic layout)."""
    if explicit is not None:
        cur = explicit.resolve()
    else:
        w = os.environ.get("ATOMADIC_WORKSPACE", "").strip()
        if w:
            cur = Path(w).resolve()
        else:
            cur = Path.cwd().resolve()

    for _ in range(40):
        if (cur / "agents" / "INDEX.md").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    script_root = Path(__file__).resolve().parents[2]
    if (script_root / "agents" / "INDEX.md").is_file():
        return script_root
    raise RuntimeError("Could not find agents/INDEX.md; pass --repo or set ATOMADIC_WORKSPACE")
