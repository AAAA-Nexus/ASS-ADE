from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SwarmServiceConfig:
    """Environment-driven configuration (defaults are conservative)."""

    repo_root: Path
    plan_rel_dir: str
    tick_interval_sec: float
    doc_regen_interval_sec: float
    nudge_cooldown_sec: float
    run_doc_regen: bool
    run_ade_harness_check: bool
    broadcast_on_ready: bool
    routes: str
    max_signals_per_day: int

    @classmethod
    def from_env(cls, repo_root: Path) -> "SwarmServiceConfig":
        plan = os.environ.get("SWARM_PLAN_DIR", "active/ass-ade-ship-nexus-github-20260422")
        return cls(
            repo_root=repo_root,
            plan_rel_dir=plan.strip().rstrip("/\\"),
            tick_interval_sec=float(os.environ.get("SWARM_TICK_SEC", "120")),
            doc_regen_interval_sec=float(os.environ.get("SWARM_DOC_REGEN_SEC", "86400")),
            nudge_cooldown_sec=float(os.environ.get("SWARM_NUDGE_COOLDOWN_SEC", "14400")),
            run_doc_regen=os.environ.get("SWARM_REGEN_DOCS", "1").strip() not in ("0", "false"),
            run_ade_harness_check=os.environ.get("SWARM_HARNESS_CHECK", "0").strip() in ("1", "true"),
            broadcast_on_ready=os.environ.get("SWARM_BROADCAST_READY", "1").strip() not in ("0", "false"),
            routes=os.environ.get("SWARM_NUDGE_ROUTES", "orchestrator,parent"),
            max_signals_per_day=int(os.environ.get("SWARM_MAX_NUDGES_DAY", "8")),
        )
