# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:124
# Component id: mo.source.ass_ade.testexceptionhandling
__version__ = "0.1.0"

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
