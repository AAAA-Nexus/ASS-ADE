# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifycomplexity.py:27
# Component id: at.source.ass_ade.test_long_text_adds_complexity
__version__ = "0.1.0"

    def test_long_text_adds_complexity(self):
        short = classify_complexity("Fix the bug")
        long_ = classify_complexity("Fix the bug " + "detailed context " * 100)
        assert long_ > short
