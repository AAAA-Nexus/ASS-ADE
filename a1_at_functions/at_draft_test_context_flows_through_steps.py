# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipeline.py:28
# Component id: at.source.ass_ade.test_context_flows_through_steps
__version__ = "0.1.0"

    def test_context_flows_through_steps(self) -> None:
        pipe = Pipeline("context")
        pipe.add("count1", counting_step)
        pipe.add("count2", counting_step)
        result = pipe.run()
        assert result.passed
        assert result.context["count"] == 2
