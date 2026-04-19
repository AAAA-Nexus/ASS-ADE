# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipeline.py:43
# Component id: at.source.ass_ade.test_chaining_add
__version__ = "0.1.0"

    def test_chaining_add(self) -> None:
        pipe = Pipeline("chain")
        returned = pipe.add("s1", pass_step).add("s2", pass_step)
        assert returned is pipe
        assert len(pipe.step_names) == 2
