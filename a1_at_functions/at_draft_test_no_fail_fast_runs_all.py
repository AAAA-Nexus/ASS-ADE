# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:109
# Component id: at.source.ass_ade.test_no_fail_fast_runs_all
__version__ = "0.1.0"

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
