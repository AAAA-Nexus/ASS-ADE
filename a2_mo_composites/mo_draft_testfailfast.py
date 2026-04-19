# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfailfast.py:5
# Component id: mo.source.ass_ade.testfailfast
__version__ = "0.1.0"

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
