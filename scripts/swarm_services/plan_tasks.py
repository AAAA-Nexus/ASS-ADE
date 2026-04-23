from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_tasks_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"tasks.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_node_map(tasks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for node in tasks.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        nid = str(node.get("id") or "").strip()
        if not nid:
            continue
        out[nid] = node
    return out


def depends_satisfied(
    node_id: str, nodes: dict[str, dict[str, Any]], state: dict[str, dict[str, Any]]
) -> bool:
    node = nodes.get(node_id)
    if not node:
        return False
    for dep in node.get("dependsOn") or []:
        d = str(dep)
        st = (state.get(d) or {}).get("status", "pending")
        if st != "done":
            return False
    return True


def node_status(
    node_id: str, nodes: dict[str, dict[str, Any]], state: dict[str, dict[str, Any]]
) -> str:
    return str((state.get(node_id) or {}).get("status") or "pending")


def ready_nodes(
    nodes: dict[str, dict[str, Any]], state: dict[str, dict[str, Any]]
) -> list[str]:
    """Node ids that are *actionable*: deps met, status pending (not done / blocked / in_progress)."""
    ready: list[str] = []
    for nid in nodes:
        st = node_status(nid, nodes, state)
        if st == "done":
            continue
        if st in ("blocked", "in_progress"):
            continue
        if depends_satisfied(nid, nodes, state):
            ready.append(nid)
    return sorted(ready, key=node_sort_key)


def node_sort_key(nid: str) -> tuple:
    if len(nid) >= 2 and nid[0] == "T" and nid[1:].isdigit():
        return (0, int(nid[1:]))
    return (1, nid)
