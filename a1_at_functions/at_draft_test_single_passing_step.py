# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipeline.py:12
# Component id: at.source.ass_ade.test_single_passing_step
__version__ = "0.1.0"

    def test_single_passing_step(self) -> None:
        pipe = Pipeline("single")
        pipe.add("step1", pass_step)
        result = pipe.run()
        assert result.passed
        assert len(result.steps) == 1
        assert result.steps[0].status == StepStatus.PASSED
