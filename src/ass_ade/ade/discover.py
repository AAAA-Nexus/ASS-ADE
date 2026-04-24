from __future__ import annotations

import os
from pathlib import Path


def find_monorepo_root(explicit: Path | None) -> Path | None:
    """Return the repo root with ``agents/INDEX.md`` if any exists."""
    if explicit is not None:
        p = explicit.resolve()
        if (p / "agents" / "INDEX.md").is_file():
            return p
        return None
    for key in ("ATOMADIC_WORKSPACE", "ASS_ADE_MONOREPO", "ASS_ADE_SOURCE"):
        raw = (os.environ.get(key) or "").strip()
        if not raw:
            continue
        p = Path(raw).resolve()
        if (p / "agents" / "INDEX.md").is_file():
            return p
    here = Path.cwd().resolve()
    for start in (here, Path(__file__).resolve().parents[4]):
        p = start
        for _ in range(20):
            if (p / "agents" / "INDEX.md").is_file():
                return p
            if p.parent == p:
                break
            p = p.parent
    return None


def ass_ade_v11_package_dir() -> Path:
    return Path(__file__).resolve().parent
