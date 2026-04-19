# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipeline.py:36
# Component id: at.source.ass_ade.test_initial_context_is_available
__version__ = "0.1.0"

    def test_initial_context_is_available(self) -> None:
        pipe = Pipeline("initial")
        pipe.add("reader", context_reader)
        result = pipe.run({"message": "hello"})
        assert result.passed
        assert result.context["reader"]["read_message"] == "hello"
