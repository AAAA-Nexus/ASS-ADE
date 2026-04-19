# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:218
# Component id: mo.source.ass_ade.testpipelineresult
__version__ = "0.1.0"

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
