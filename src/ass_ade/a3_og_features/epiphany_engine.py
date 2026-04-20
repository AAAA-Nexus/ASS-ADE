"""Tier a3_og — Epiphany Engine: analyze a materialized codebase and generate an improvement plan.

Wraps the engine's Epiphany analysis pass. Produces a structured plan (list of
ForgeTask experiments) that the ForgeLoop then executes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class EpiphanyEngine:
    """Idea-to-plan pipeline for code improvement.

    Usage::

        engine = EpiphanyEngine(idea="Improve Flask API", sources=[str(target)])
        engine.run_recon(target)
        engine.generate_breakthrough()
        ok, reason = engine.check_promotion()
        if ok:
            plan = engine.plan()  # ready to hand to ForgeLoop
    """

    idea: str
    sources: list[str] = field(default_factory=list)
    _recon: dict[str, Any] = field(default_factory=dict, init=False)
    _breakthrough: dict[str, Any] = field(default_factory=dict, init=False)
    _epiphany_plan: Any = field(default=None, init=False)

    def run_recon(self, cwd: Path | None = None) -> dict[str, Any]:
        """Gather local signals: file count, Python file count, path."""
        cwd = cwd or Path(".")
        self._recon = {
            "idea": self.idea,
            "cwd": str(cwd),
            "py_files": len(list(cwd.rglob("*.py"))),
        }
        return self._recon

    def generate_breakthrough(self, target_root: Path | None = None) -> dict[str, Any]:
        """Run the Epiphany AST analysis pass and build a task list.

        If *target_root* is provided, performs real AST-based analysis via
        the engine's ``generate_plan``. Otherwise falls back to a stub plan.
        """
        if target_root is not None:
            from ass_ade.engine.rebuild.forge import generate_plan

            self._epiphany_plan = generate_plan(target_root)
            experiments = [
                {
                    "id": t.task_id,
                    "file": t.file,
                    "node": t.node,
                    "issue": t.issue,
                    "instruction": t.instruction,
                }
                for t in self._epiphany_plan.experiments
            ]
        else:
            experiments = []
            self._epiphany_plan = None

        self._breakthrough = {
            "idea": self.idea,
            "experiments": experiments,
            "vetted_sources": self.sources,
            "promoted": len(self.sources) > 0 and len(experiments) > 0,
        }
        return self._breakthrough

    def check_promotion(self) -> tuple[bool, str]:
        """Gate: blocks advancement if no vetted sources or no experiments."""
        if not self._breakthrough:
            return False, "generate_breakthrough must be called first"
        if not self._breakthrough.get("vetted_sources"):
            return False, "promotion blocked - no vetted sources supplied"
        if not self._breakthrough.get("experiments"):
            return False, "promotion blocked - no improvement experiments found"
        return True, "promoted"

    def plan(self) -> dict[str, Any]:
        """Emit the structured Epiphany plan if promotion passes."""
        ok, reason = self.check_promotion()
        if not ok:
            raise RuntimeError(f"Epiphany gate: {reason}")
        return {
            "schema": "atomadic.epiphany-plan.v1",
            "idea": self.idea,
            "recon": self._recon,
            "breakthrough": self._breakthrough,
            "engine_plan": self._epiphany_plan,
            "status": "ready",
        }
