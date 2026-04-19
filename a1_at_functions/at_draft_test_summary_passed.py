# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:219
# Component id: at.source.ass_ade.test_summary_passed
__version__ = "0.1.0"

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
