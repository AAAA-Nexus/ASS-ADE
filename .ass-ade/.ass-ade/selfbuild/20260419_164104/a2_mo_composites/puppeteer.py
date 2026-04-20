"""v18 pillar 88 — Puppeteer RL orchestrator with DAG fallback."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class AgentRef:
    name: str
    priority: float
    reason: str = ""


_DEFAULT_DAG: list[tuple[str, float]] = [
    ("sam", 0.95),
    ("map_terrain", 0.90),
    ("atlas", 0.85),
    ("alphaverus", 0.80),
    ("proofbridge", 0.75),
    ("wisdom", 0.70),
    ("dgm_h", 0.65),
]


class Puppeteer:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        cfg = config.get("puppeteer") or {}
        self._policy_path = Path(cfg.get("policy_path", ".ass-ade/policies/puppeteer.pt"))
        self._fallback_dag = bool(cfg.get("fallback_to_dag", True))
        self._dag = list(_DEFAULT_DAG)
        self._selections = 0

    def _policy_available(self) -> bool:
        return self._policy_path.exists()

    def select_next_agent(self, state: dict) -> AgentRef:
        self._selections += 1
        visited = set(state.get("visited", []))
        if self._policy_available():
            return AgentRef(name="policy", priority=1.0, reason="rl_policy")
        if not self._fallback_dag:
            return AgentRef(name="noop", priority=0.0, reason="no_policy_no_dag")
        for name, prio in self._dag:
            if name not in visited:
                return AgentRef(name=name, priority=prio, reason="dag_fallback")
        return AgentRef(name="done", priority=0.0, reason="dag_exhausted")

    def run(self, ctx: dict) -> dict:
        agent = self.select_next_agent(ctx)
        return {"next": agent.name, "priority": agent.priority, "reason": agent.reason}

    def report(self) -> dict:
        return {
            "engine": "puppeteer",
            "policy_available": self._policy_available(),
            "fallback_enabled": self._fallback_dag,
            "selections": self._selections,
        }
