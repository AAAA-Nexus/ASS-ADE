# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifycomplexity.py:21
# Component id: at.source.ass_ade.test_formal_verification
__version__ = "0.1.0"

    def test_formal_verification(self):
        c = classify_complexity(
            "Write a formal proof that this invariant holds across all states"
        )
        assert c >= 0.2  # formal keywords detected
