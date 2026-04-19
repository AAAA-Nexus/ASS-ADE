# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testauditquestions.py:13
# Component id: at.source.ass_ade.test_ids_are_1_to_50
__version__ = "0.1.0"

    def test_ids_are_1_to_50(self) -> None:
        ids = sorted(q["id"] for q in AUDIT_QUESTIONS)
        assert ids == list(range(1, 51))
