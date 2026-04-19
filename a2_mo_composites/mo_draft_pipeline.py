# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:101
# Component id: mo.source.ass_ade.pipeline
from __future__ import annotations

__version__ = "0.1.0"

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
