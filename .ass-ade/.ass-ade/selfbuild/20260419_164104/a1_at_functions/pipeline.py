"""Async workflow pipeline — composable, chainable hero workflows.

A Pipeline is a sequence of Steps that execute in order, with each step
receiving the accumulated context from prior steps. Pipelines support:

  - Sequential execution with context passing
  - Early termination on step failure (with configurable policy)
  - Result persistence to .ass-ade/workflows/
  - Progress callbacks for CLI and editor integration
  - Composability: pipelines can be nested as steps

Formal model:
    Let P = (s₁, s₂, ..., sₙ) be a pipeline.
    Each sᵢ: Context → StepResult.
    Context accumulates: ctx₀ → s₁(ctx₀) → ctx₁ → s₂(ctx₁) → ... → ctxₙ

    If fail_fast=True:
        ∃ sᵢ: failed(sᵢ) ⟹ ∀ j > i: skipped(sⱼ)

Usage:
    pipe = Pipeline("my-workflow")
    pipe.add("scan", scan_step)
    pipe.add("certify", certify_step)
    result = pipe.run(initial_context)
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """Result of a single pipeline step."""

    name: str
    status: StepStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration_ms: float = 0.0


@dataclass
class PipelineResult:
    """Result of an entire pipeline execution."""

    name: str
    steps: list[StepResult] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    passed: bool = False
    duration_ms: float = 0.0

    @property
    def failed_steps(self) -> list[StepResult]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    @property
    def summary(self) -> str:
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s.status == StepStatus.PASSED)
        failed = sum(1 for s in self.steps if s.status == StepStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == StepStatus.SKIPPED)
        verdict = "PASSED" if self.passed else "FAILED"
        return f"[{verdict}] {self.name}: {passed}/{total} passed, {failed} failed, {skipped} skipped ({self.duration_ms:.0f}ms)"


class StepFunction(Protocol):
    """Protocol for pipeline step functions.

    Takes a mutable context dict, performs work, and returns a StepResult.
    The step may add keys to context for downstream steps.
    """

    def __call__(self, context: dict[str, Any]) -> StepResult: ...


# Progress callback type
ProgressCallback = Callable[[str, StepStatus, int, int], None]


@dataclass
class _StepEntry:
    name: str
    fn: StepFunction


class Pipeline:
    """Composable workflow pipeline with sequential step execution.

    Steps are functions that take a context dict and return a StepResult.
    Context is shared across all steps, allowing data to flow through
    the pipeline.
    """

    def __init__(
        self,
        name: str,
        *,
        fail_fast: bool = True,
        persist_dir: str | None = None,
        on_progress: ProgressCallback | None = None,
    ) -> None:
        self._name = name
        self._steps: list[_StepEntry] = []
        self._fail_fast = fail_fast
        self._persist_dir = persist_dir
        self._on_progress = on_progress

    @property
    def name(self) -> str:
        return self._name

    @property
    def step_names(self) -> list[str]:
        return [s.name for s in self._steps]

    def add(self, name: str, fn: StepFunction) -> Pipeline:
        """Add a step to the pipeline. Returns self for chaining."""
        self._steps.append(_StepEntry(name=name, fn=fn))
        return self

    def run(self, context: dict[str, Any] | None = None) -> PipelineResult:
        """Execute the pipeline sequentially.

        Returns the full PipelineResult with all step outcomes.
        """
        ctx = dict(context or {})
        results: list[StepResult] = []
        total = len(self._steps)
        pipeline_start = time.monotonic()
        should_skip = False

        for i, entry in enumerate(self._steps):
            if should_skip:
                sr = StepResult(name=entry.name, status=StepStatus.SKIPPED)
                results.append(sr)
                if self._on_progress:
                    self._on_progress(entry.name, StepStatus.SKIPPED, i + 1, total)
                continue

            if self._on_progress:
                self._on_progress(entry.name, StepStatus.RUNNING, i + 1, total)

            step_start = time.monotonic()
            try:
                sr = entry.fn(ctx)
                if not sr.duration_ms:
                    sr.duration_ms = (time.monotonic() - step_start) * 1000
            except Exception as exc:
                sr = StepResult(
                    name=entry.name,
                    status=StepStatus.FAILED,
                    error=str(exc),
                    duration_ms=(time.monotonic() - step_start) * 1000,
                )

            # Ensure name matches
            sr.name = entry.name
            results.append(sr)

            # Merge step output into shared context
            if sr.output:
                ctx[entry.name] = sr.output

            if self._on_progress:
                self._on_progress(entry.name, sr.status, i + 1, total)

            if sr.status == StepStatus.FAILED and self._fail_fast:
                should_skip = True

        pipeline_duration = (time.monotonic() - pipeline_start) * 1000
        all_passed = all(s.status in (StepStatus.PASSED, StepStatus.SKIPPED) for s in results)
        no_failures = not any(s.status == StepStatus.FAILED for s in results)

        result = PipelineResult(
            name=self._name,
            steps=results,
            context=ctx,
            passed=bool(results) and all_passed and no_failures,
            duration_ms=pipeline_duration,
        )

        # Persist result if configured
        if self._persist_dir:
            self._persist(result)

        return result

    def _persist(self, result: PipelineResult) -> None:
        """Save pipeline result to disk."""
        out_dir = Path(self._persist_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = time.time_ns()
        filename = f"{self._name}_{ts}.json"
        data = {
            "name": result.name,
            "passed": result.passed,
            "duration_ms": result.duration_ms,
            "steps": [
                {
                    "name": s.name,
                    "status": s.status.value,
                    "output": s.output,
                    "error": s.error,
                    "duration_ms": s.duration_ms,
                }
                for s in result.steps
            ],
        }
        (out_dir / filename).write_text(json.dumps(data, indent=2), encoding="utf-8")


# ── Pre-built pipeline constructors ──────────────────────────────────────────


def trust_gate_pipeline(
    client: Any,
    agent_id: str,
    *,
    on_progress: ProgressCallback | None = None,
    persist_dir: str | None = None,
) -> Pipeline:
    """Build a trust-gate pipeline: identity → sybil → trust → reputation → gate.

    Uses NexusClient endpoints, wrapping each as a pipeline step.
    """
    from ass_ade.nexus.validation import validate_agent_id

    aid = validate_agent_id(agent_id)

    def identity_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.identity_verify(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("decision", "allow") != "deny"
            ctx["identity_passed"] = passed
            return StepResult(name="identity_verify", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="identity_verify", status=StepStatus.FAILED, error=str(exc))

    def sybil_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.sybil_check(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            risk = raw.get("sybil_risk", "low")
            passed = risk != "high"
            ctx["sybil_passed"] = passed
            return StepResult(name="sybil_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="sybil_check", status=StepStatus.FAILED, error=str(exc))

    def trust_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.trust_score(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            score = raw.get("score", 0)
            passed = score >= 0.5
            ctx["trust_score"] = score
            return StepResult(name="trust_score", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="trust_score", status=StepStatus.FAILED, error=str(exc))

    def reputation_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.reputation_score(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["reputation_tier"] = raw.get("tier")
            return StepResult(name="reputation_score", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="reputation_score", status=StepStatus.FAILED, error=str(exc))

    def gate_step(ctx: dict[str, Any]) -> StepResult:
        trust_score = ctx.get("trust_score", 0)
        rep_tier = ctx.get("reputation_tier")
        identity_ok = ctx.get("identity_passed", False)
        sybil_ok = ctx.get("sybil_passed", False)

        if not identity_ok or not sybil_ok:
            verdict = "DENY"
        elif trust_score < 0.5:
            verdict = "DENY"
        elif trust_score < 0.7 and rep_tier not in {"gold", "platinum"}:
            verdict = "WARN"
        else:
            verdict = "ALLOW"

        ctx["verdict"] = verdict
        passed = verdict != "DENY"
        return StepResult(
            name="gate_decision",
            status=StepStatus.PASSED if passed else StepStatus.FAILED,
            output={"verdict": verdict, "trust_score": trust_score, "reputation_tier": rep_tier},
        )

    pipe = Pipeline(
        f"trust-gate-{aid}",
        fail_fast=False,  # run all steps even if some fail
        persist_dir=persist_dir,
        on_progress=on_progress,
    )
    pipe.add("identity_verify", identity_step)
    pipe.add("sybil_check", sybil_step)
    pipe.add("trust_score", trust_step)
    pipe.add("reputation_score", reputation_step)
    pipe.add("gate_decision", gate_step)
    return pipe


def certify_pipeline(
    client: Any,
    text: str,
    *,
    on_progress: ProgressCallback | None = None,
    persist_dir: str | None = None,
) -> Pipeline:
    """Build a certification pipeline: hallucination → ethics → compliance → certify."""

    def hallucination_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.hallucination_oracle(text)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            verdict = raw.get("verdict", "unknown")
            passed = verdict not in ("unsafe", "error")
            ctx["hallucination_verdict"] = verdict
            return StepResult(name="hallucination_oracle", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="hallucination_oracle", status=StepStatus.FAILED, error=str(exc))

    def ethics_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.ethics_check(text)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("safe", False)
            return StepResult(name="ethics_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="ethics_check", status=StepStatus.FAILED, error=str(exc))

    def compliance_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.compliance_check(text)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("compliant", False)
            return StepResult(name="compliance_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="compliance_check", status=StepStatus.FAILED, error=str(exc))

    def certify_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["certificate_id"] = raw.get("certificate_id")
            return StepResult(name="certify_output", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="certify_output", status=StepStatus.FAILED, error=str(exc))

    pipe = Pipeline(
        "certify-output",
        fail_fast=False,
        persist_dir=persist_dir,
        on_progress=on_progress,
    )
    pipe.add("hallucination_oracle", hallucination_step)
    pipe.add("ethics_check", ethics_step)
    pipe.add("compliance_check", compliance_step)
    pipe.add("certify_output", certify_step)
    return pipe
