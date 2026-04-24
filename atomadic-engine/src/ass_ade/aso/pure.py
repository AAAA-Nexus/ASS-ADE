"""a1 pure helpers for ASO — no side effects."""

from __future__ import annotations

import re
from pathlib import Path

_TOPOLOGY_PATTERN = re.compile(r"^(parallel|sequential|hierarchical|adaptive)$")


def is_valid_topology(value: str) -> bool:
    return bool(_TOPOLOGY_PATTERN.match(value.strip()))


def normalize_repo_root(raw: Path | str) -> Path:
    return Path(raw).resolve()


def aso_layout_paths(repo_root: Path) -> dict[str, Path]:
    base = repo_root / ".ass-ade" / "aso"
    swarm = repo_root / ".ass-ade" / "swarm"
    graph = repo_root / ".ass-ade" / "graph"
    return {
        "aso_root": base,
        "swarm_config": swarm / "config.json",
        "graph_dir": graph,
        "schemas": base,
        "logs": base / "logs",
    }


def merge_swarm_config_payload(
    existing: dict[str, object] | None,
    *,
    topology: str,
    shared_memory_endpoint: str | None,
    notes: str | None = None,
) -> dict[str, object]:
    out: dict[str, object] = dict(existing or {})
    out["topology"] = topology
    if shared_memory_endpoint is not None:
        out["shared_memory_endpoint"] = shared_memory_endpoint
    if notes:
        out["notes"] = notes
    out.setdefault("schema", "ass-ade.swarm-config.v0")
    return out
