"""Tier a1 — pure ``Path`` helpers for autopoiesis topic directories (no I/O)."""

from __future__ import annotations

import json
from pathlib import Path

from ass_ade.engine.rebuild.autopoiesis_constants import (
    AUTOPOIESIS_TOPICS,
    EPISODE_SCHEMA_VERSION,
    MEMORY_EPISODES_FILE,
    MEMORY_ROOT_REL,
)


def autopoiesis_memory_root(repo_root: Path) -> Path:
    """Return ``<repo>/.ass-ade/memory`` as a path object."""
    base = repo_root
    for part in MEMORY_ROOT_REL:
        base /= part
    return base


def iter_autopoiesis_topic_paths(repo_root: Path) -> tuple[Path, ...]:
    """Return topic shard paths (codebase, user, workspace, memory)."""
    root = autopoiesis_memory_root(repo_root)
    return tuple(root / name for name in AUTOPOIESIS_TOPICS)


def episodes_jsonl_path(repo_root: Path) -> Path:
    """Return path to the append-only Forge / autopoiesis episode log."""
    return autopoiesis_memory_root(repo_root) / MEMORY_EPISODES_FILE


def format_package_emit_episode_line(
    *,
    utc_iso: str,
    vendored_ass_ade: bool,
    hatch_wheel_packages: list[str],
) -> str:
    """One JSON object per line for ``episodes.jsonl`` (no secrets, no raw env)."""
    payload = {
        "schema_version": EPISODE_SCHEMA_VERSION,
        "ts": utc_iso,
        "event": "package_emit",
        "vendored_ass_ade": vendored_ass_ade,
        "hatch_wheel_packages": list(hatch_wheel_packages),
        "evidence": [
            "src/ass_ade/engine/rebuild/package_emitter.py",
            "src/ass_ade/engine/rebuild/autopoiesis_layout.py",
        ],
        "rollback_hint": (
            "git checkout -- src/ass_ade/engine/rebuild/package_emitter.py "
            "src/ass_ade/engine/rebuild/autopoiesis_layout.py "
            "src/ass_ade/engine/rebuild/autopoiesis_constants.py; "
            "truncate or remove .ass-ade/memory/episodes.jsonl"
        ),
    }
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
