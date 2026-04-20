"""Tier a3_og — Forge Loop: execute an Epiphany plan as parallel focused LLM tasks.

Takes the structured plan from EpiphanyEngine and runs each improvement task as
a single focused LLM call. Tasks on different files run in parallel via
ThreadPoolExecutor; tasks on the same file run sequentially to avoid line-number
drift from concurrent writes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.swarm_types import Episode


@dataclass
class ForgeLoop:
    """Execute an Epiphany improvement plan in parallel LLM calls.

    Each task = one function/class + one issue + one LLM call.
    Results are recorded as Episodes for swarm lineage.

    Usage::

        loop = ForgeLoop(cwd=target_root, model="qwen3:8b-fp16")
        result = loop.run_plan(epiphany_plan)
        episodes = loop.episodes  # list of Episode records
    """

    cwd: Path = field(default_factory=Path)
    model: str = "qwen3:8b-fp16"
    max_workers: int = 4
    episodes: list[Episode] = field(default_factory=list)

    def run_plan(self, epiphany_plan: dict[str, Any]) -> dict[str, Any]:
        """Execute all tasks in the Epiphany plan.

        Args:
            epiphany_plan: dict from ``EpiphanyEngine.plan()`` containing the
                           engine-level ``EpiphanyPlan`` under ``engine_plan``.

        Returns:
            ForgeResult summary dict (tasks, applied, skipped, files_modified).
        """
        import time

        from ass_ade.engine.rebuild.forge import execute_plan

        engine_plan = epiphany_plan.get("engine_plan")
        if engine_plan is None:
            return {
                "tasks": 0,
                "applied": 0,
                "skipped": 0,
                "files_modified": 0,
                "error": "engine_plan not set - call EpiphanyEngine.generate_breakthrough(target_root) first",
            }

        start = time.monotonic()
        forge_result = execute_plan(engine_plan, model=self.model, max_workers=self.max_workers)
        duration_ms = int((time.monotonic() - start) * 1000)

        for task_result in forge_result.results:
            if task_result.verified:
                episode: Episode = {
                    "goal": f"fix:{task_result.issue}:{task_result.node}",
                    "tools_used": ["ollama", self.model],
                    "key_files": [task_result.file],
                    "verdict": "PASS",
                    "duration_ms": duration_ms // max(len(forge_result.results), 1),
                    "notes": task_result.diff_summary,
                }
                self.episodes.append(episode)

        summary = {
            "tasks": forge_result.plan_tasks,
            "applied": forge_result.applied,
            "skipped": forge_result.skipped,
            "files_modified": len(forge_result.files_modified),
            "model": forge_result.model_used,
            "episodes": len(self.episodes),
        }
        return summary

    def run_full(self, target_root: Path) -> dict[str, Any]:
        """Convenience: run Epiphany analysis + ForgeLoop execution in one call.

        Args:
            target_root: Path to the materialized output directory.

        Returns:
            Summary dict with plan tasks, applied fixes, and episodes recorded.
        """
        from ass_ade.a3_og_features.epiphany_engine import EpiphanyEngine

        engine = EpiphanyEngine(
            idea=f"Improve codebase at {target_root.name}",
            sources=[str(target_root)],
        )
        engine.run_recon(target_root)
        engine.generate_breakthrough(target_root)
        ok, reason = engine.check_promotion()
        if not ok:
            return {
                "tasks": 0,
                "applied": 0,
                "skipped": 0,
                "files_modified": 0,
                "error": reason,
            }

        plan = engine.plan()
        return self.run_plan(plan)

    # Legacy interface (kept for compatibility).

    def propose_goals(self, topic: str | None = None) -> list[str]:
        """Return improvement goal strings (legacy interface)."""
        from ass_ade.engine.rebuild.forge import generate_plan

        if not self.cwd.exists():
            return []
        plan = generate_plan(self.cwd)
        return [f"{t.issue}:{t.node}" for t in plan.experiments]

    def verify(self) -> tuple[bool, str]:
        """Run pytest in cwd. Returns (passed, summary_line)."""
        import subprocess

        result = subprocess.run(
            ["python", "-m", "pytest", "--tb=no", "-q"],
            capture_output=True,
            text=True,
            cwd=self.cwd,
        )
        passed = result.returncode == 0
        last = (
            result.stdout.strip().splitlines()[-1]
            if result.stdout.strip()
            else "no output"
        )
        return passed, last

    def record_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)
