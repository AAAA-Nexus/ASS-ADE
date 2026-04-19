# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testauditquestions.py:23
# Component id: at.source.ass_ade.test_all_have_required_keys
__version__ = "0.1.0"

    def test_all_have_required_keys(self) -> None:
        for q in AUDIT_QUESTIONS:
            assert "id" in q and "group" in q and "text" in q
            assert isinstance(q["text"], str) and q["text"]
