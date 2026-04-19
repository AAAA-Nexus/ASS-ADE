# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipeline.py:20
# Component id: at.source.ass_ade.test_single_failing_step
__version__ = "0.1.0"

    def test_single_failing_step(self) -> None:
        pipe = Pipeline("fail")
        pipe.add("step1", fail_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert result.steps[0].error == "something broke"
