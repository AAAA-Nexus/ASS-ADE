# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifycomplexity.py:32
# Component id: at.source.ass_ade.test_range_bounded
__version__ = "0.1.0"

    def test_range_bounded(self):
        c = classify_complexity(
            "First implement a function, then write a theorem proof, "
            "design the architecture, and create several test files " * 10
        )
        assert c <= 1.0
