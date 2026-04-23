"""Tests for the async workflow pipeline engine."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ass_ade.pipeline import (
    Pipeline,
    PipelineResult,
    StepResult,
    StepStatus,
)

# ── Helpers ──────────────────────────────────────────────────────────────────


def pass_step(ctx: dict[str, Any]) -> StepResult:
    ctx["pass_ran"] = True
    return StepResult(name="pass", status=StepStatus.PASSED, output={"ok": True})


def fail_step(ctx: dict[str, Any]) -> StepResult:
    return StepResult(name="fail", status=StepStatus.FAILED, error="something broke")


def counting_step(ctx: dict[str, Any]) -> StepResult:
    count = ctx.get("count", 0)
    ctx["count"] = count + 1
    return StepResult(name="count", status=StepStatus.PASSED, output={"count": count + 1})


def error_step(ctx: dict[str, Any]) -> StepResult:
    raise RuntimeError("kaboom")


def context_reader(ctx: dict[str, Any]) -> StepResult:
    """Step that reads 'message' from context."""
    msg = ctx.get("message", "")
    return StepResult(
        name="reader", status=StepStatus.PASSED, output={"read_message": msg}
    )


# ── Pipeline basics ──────────────────────────────────────────────────────────


class TestPipeline:
    def test_empty_pipeline_fails(self) -> None:
        pipe = Pipeline("empty")
        result = pipe.run()
        assert not result.passed
        assert len(result.steps) == 0

    def test_single_passing_step(self) -> None:
        pipe = Pipeline("single")
        pipe.add("step1", pass_step)
        result = pipe.run()
        assert result.passed
        assert len(result.steps) == 1
        assert result.steps[0].status == StepStatus.PASSED

    def test_single_failing_step(self) -> None:
        pipe = Pipeline("fail")
        pipe.add("step1", fail_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert result.steps[0].error == "something broke"

    def test_context_flows_through_steps(self) -> None:
        pipe = Pipeline("context")
        pipe.add("count1", counting_step)
        pipe.add("count2", counting_step)
        result = pipe.run()
        assert result.passed
        assert result.context["count"] == 2

    def test_initial_context_is_available(self) -> None:
        pipe = Pipeline("initial")
        pipe.add("reader", context_reader)
        result = pipe.run({"message": "hello"})
        assert result.passed
        assert result.context["reader"]["read_message"] == "hello"

    def test_chaining_add(self) -> None:
        pipe = Pipeline("chain")
        returned = pipe.add("s1", pass_step).add("s2", pass_step)
        assert returned is pipe
        assert len(pipe.step_names) == 2


# ── Fail-fast mode ───────────────────────────────────────────────────────────


class TestFailFast:
    def test_fail_fast_skips_remaining(self) -> None:
        pipe = Pipeline("ff", fail_fast=True)
        pipe.add("s1", pass_step)
        pipe.add("s2", fail_step)
        pipe.add("s3", pass_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.PASSED
        assert result.steps[1].status == StepStatus.FAILED
        assert result.steps[2].status == StepStatus.SKIPPED

    def test_no_fail_fast_runs_all(self) -> None:
        pipe = Pipeline("noff", fail_fast=False)
        pipe.add("s1", pass_step)
        pipe.add("s2", fail_step)
        pipe.add("s3", pass_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.PASSED
        assert result.steps[1].status == StepStatus.FAILED
        assert result.steps[2].status == StepStatus.PASSED


# ── Exception handling ───────────────────────────────────────────────────────


class TestExceptionHandling:
    def test_exception_becomes_failed_step(self) -> None:
        pipe = Pipeline("err")
        pipe.add("boom", error_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert "kaboom" in result.steps[0].error

    def test_exception_with_fail_fast(self) -> None:
        pipe = Pipeline("errff", fail_fast=True)
        pipe.add("s1", pass_step)
        pipe.add("s2", error_step)
        pipe.add("s3", pass_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[2].status == StepStatus.SKIPPED


# ── Progress callback ────────────────────────────────────────────────────────


class TestProgressCallback:
    def test_callback_is_called(self) -> None:
        calls: list[tuple[str, StepStatus, int, int]] = []

        def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
            calls.append((name, status, current, total))

        pipe = Pipeline("prog", on_progress=on_progress)
        pipe.add("s1", pass_step)
        pipe.add("s2", pass_step)
        pipe.run()

        # Each step: RUNNING then PASSED = 2 calls per step = 4 total
        assert len(calls) == 4
        assert calls[0] == ("s1", StepStatus.RUNNING, 1, 2)
        assert calls[1] == ("s1", StepStatus.PASSED, 1, 2)
        assert calls[2] == ("s2", StepStatus.RUNNING, 2, 2)
        assert calls[3] == ("s2", StepStatus.PASSED, 2, 2)

    def test_callback_on_skip(self) -> None:
        calls: list[tuple[str, StepStatus, int, int]] = []

        def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
            calls.append((name, status, current, total))

        pipe = Pipeline("skip", fail_fast=True, on_progress=on_progress)
        pipe.add("s1", fail_step)
        pipe.add("s2", pass_step)
        pipe.run()

        statuses = [s for _, s, _, _ in calls]
        assert StepStatus.SKIPPED in statuses


# ── Persistence ──────────────────────────────────────────────────────────────


class TestPersistence:
    def test_persist_creates_file(self, tmp_path: Path) -> None:
        pipe = Pipeline("persist", persist_dir=str(tmp_path))
        pipe.add("s1", pass_step)
        pipe.run()

        files = list(tmp_path.glob("persist_*.json"))
        assert len(files) == 1

        data = json.loads(files[0].read_text())
        assert data["name"] == "persist"
        assert data["passed"] is True
        assert len(data["steps"]) == 1

    def test_persist_records_failure(self, tmp_path: Path) -> None:
        pipe = Pipeline("failp", persist_dir=str(tmp_path))
        pipe.add("s1", fail_step)
        pipe.run()

        files = list(tmp_path.glob("failp_*.json"))
        data = json.loads(files[0].read_text())
        assert data["passed"] is False
        assert data["steps"][0]["error"] == "something broke"

    def test_no_persist_when_not_configured(self, tmp_path: Path) -> None:
        pipe = Pipeline("nopersist")
        pipe.add("s1", pass_step)
        pipe.run()
        # No files created anywhere — this is just a sanity check
        assert not list(tmp_path.glob("*.json"))


# ── PipelineResult ───────────────────────────────────────────────────────────


class TestPipelineResult:
    def test_summary_passed(self) -> None:
        result = PipelineResult(
            name="test",
            steps=[
                StepResult(name="s1", status=StepStatus.PASSED),
                StepResult(name="s2", status=StepStatus.PASSED),
            ],
            passed=True,
            duration_ms=150.0,
        )
        assert "[PASSED]" in result.summary
        assert "2/2 passed" in result.summary

    def test_summary_failed(self) -> None:
        result = PipelineResult(
            name="test",
            steps=[
                StepResult(name="s1", status=StepStatus.PASSED),
                StepResult(name="s2", status=StepStatus.FAILED, error="x"),
                StepResult(name="s3", status=StepStatus.SKIPPED),
            ],
            passed=False,
            duration_ms=200.0,
        )
        assert "[FAILED]" in result.summary
        assert "1 failed" in result.summary
        assert "1 skipped" in result.summary

    def test_failed_steps_property(self) -> None:
        result = PipelineResult(
            name="test",
            steps=[
                StepResult(name="s1", status=StepStatus.PASSED),
                StepResult(name="s2", status=StepStatus.FAILED),
            ],
            passed=False,
        )
        assert len(result.failed_steps) == 1
        assert result.failed_steps[0].name == "s2"

    def test_duration_tracking(self) -> None:
        pipe = Pipeline("dur")
        pipe.add("s1", pass_step)
        result = pipe.run()
        assert result.duration_ms >= 0
        assert result.steps[0].duration_ms >= 0


# ── Step names ───────────────────────────────────────────────────────────────


class TestStepNames:
    def test_step_names_property(self) -> None:
        pipe = Pipeline("names")
        pipe.add("alpha", pass_step)
        pipe.add("beta", pass_step)
        pipe.add("gamma", fail_step)
        assert pipe.step_names == ["alpha", "beta", "gamma"]

    def test_name_property(self) -> None:
        pipe = Pipeline("my-pipeline")
        assert pipe.name == "my-pipeline"
