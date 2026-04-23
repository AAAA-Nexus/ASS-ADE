from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ISO = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class DaemonState:
    """Service-wide state (tick counts, nudge dedup)."""

    last_tick_utc: str = ""
    tick_count: int = 0
    last_doc_regen_utc: str = ""
    nudge_counts_utc_date: str = ""  # YYYY-MM-DD for daily cap
    nudge_count_today: int = 0
    nudged_nodes: dict[str, str] = field(default_factory=dict)  # node_id -> last nudge ISO

    @classmethod
    def load(cls, path: Path) -> "DaemonState":
        if not path.is_file():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()
        nudged = raw.get("nudged_nodes") or {}
        if not isinstance(nudged, dict):
            nudged = {}
        return cls(
            last_tick_utc=str(raw.get("last_tick_utc") or ""),
            tick_count=int(raw.get("tick_count") or 0),
            last_doc_regen_utc=str(raw.get("last_doc_regen_utc") or ""),
            nudge_counts_utc_date=str(raw.get("nudge_counts_utc_date") or ""),
            nudge_count_today=int(raw.get("nudge_count_today") or 0),
            nudged_nodes={str(k): str(v) for k, v in nudged.items()},
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).strftime(ISO)


@dataclass
class TaskStateFile:
    """Per-plan task completion: ``nodes`` id -> {status, updated, note}."""

    plan_slug: str = ""
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def path_for_plan(cls, plan_dir: Path) -> Path:
        return plan_dir / "swarm_task_state.json"

    @classmethod
    def load(cls, plan_dir: Path) -> "TaskStateFile":
        p = cls.path_for_plan(plan_dir)
        if not p.is_file():
            return cls()
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()
        nodes = raw.get("nodes")
        if not isinstance(nodes, dict):
            nodes = {}
        return cls(
            plan_slug=str(raw.get("planSlug") or raw.get("plan_slug") or ""),
            nodes={str(k): dict(v) for k, v in nodes.items() if isinstance(v, dict)},
        )

    def save(self, plan_dir: Path) -> None:
        p = self.path_for_plan(plan_dir)
        p.parent.mkdir(parents=True, exist_ok=True)
        if not self.plan_slug:
            self.plan_slug = plan_dir.name
        out = {
            "schemaVersion": "ato.swarm_task_state.v1",
            "planSlug": self.plan_slug,
            "updated": _now(),
            "nodes": self.nodes,
        }
        p.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
