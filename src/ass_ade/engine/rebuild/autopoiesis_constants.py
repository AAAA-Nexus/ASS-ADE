"""Tier a0 — autopoiesis topic names and path fragments for ``.ass-ade/memory`` shards."""

from __future__ import annotations

# Path under repo root: <root> / .ass-ade / memory / <topic> /
MEMORY_ROOT_REL: tuple[str, ...] = (".ass-ade", "memory")

# Four bootstrapping topics (ASS-ADE autopoiesis playbook).
TOPIC_CODEBASE: str = "codebase"
TOPIC_USER: str = "user"
TOPIC_WORKSPACE: str = "workspace"
TOPIC_MEMORY: str = "memory"

AUTOPOIESIS_TOPICS: tuple[str, ...] = (
    TOPIC_CODEBASE,
    TOPIC_USER,
    TOPIC_WORKSPACE,
    TOPIC_MEMORY,
)

# Append-only lineage slice (Forge Loop v0 hook) under ``.ass-ade/memory/``.
MEMORY_EPISODES_FILE: str = "episodes.jsonl"
EPISODE_SCHEMA_VERSION: str = "ass-ade.autopoiesis.episode.v1"
