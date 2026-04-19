"""v18 pillar 86 — ATLAS task decomposition for complex specs."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SubTask:
    id: str
    description: str
    priority: float
    deps: list[str] = field(default_factory=list)


class Atlas:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._threshold = float((config.get("atlas") or {}).get("complexity_threshold", 0.7))
        self._decompositions = 0

    @staticmethod
    def complexity_score(spec: str, fan_out: int = 0) -> float:
        return len(spec) / 1000.0 + fan_out / 10.0

    def decompose(self, task: str, complexity: float | None = None) -> list[SubTask]:
        score = complexity if complexity is not None else self.complexity_score(task)
        if score <= self._threshold:
            return [SubTask(id="t0", description=task, priority=1.0)]
        self._decompositions += 1
        chunks = [c.strip() for c in task.split(".") if c.strip()]
        if len(chunks) < 2:
            mid = max(1, len(task) // 2)
            chunks = [task[:mid].strip(), task[mid:].strip()]
        subs: list[SubTask] = []
        prev: str | None = None
        for i, chunk in enumerate(chunks):
            sid = f"t{i}"
            deps = [prev] if prev else []
            subs.append(SubTask(id=sid, description=chunk, priority=1.0 - i * 0.1, deps=deps))
            prev = sid
        return subs

    def run(self, ctx: dict) -> dict:
        task = ctx.get("task", "")
        complexity = ctx.get("complexity")
        subs = self.decompose(task, complexity)
        return {
            "complexity": self.complexity_score(task, int(ctx.get("fan_out", 0))),
            "subtasks": [s.__dict__ for s in subs],
        }

    def report(self) -> dict:
        return {
            "engine": "atlas",
            "threshold": self._threshold,
            "decompositions": self._decompositions,
        }
