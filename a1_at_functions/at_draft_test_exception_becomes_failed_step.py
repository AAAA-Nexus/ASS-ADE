# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:125
# Component id: at.source.ass_ade.test_exception_becomes_failed_step
__version__ = "0.1.0"

    def test_exception_becomes_failed_step(self) -> None:
        pipe = Pipeline("err")
        pipe.add("boom", error_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert "kaboom" in result.steps[0].error
