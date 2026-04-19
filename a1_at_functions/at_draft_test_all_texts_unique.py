# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testauditquestions.py:9
# Component id: at.source.ass_ade.test_all_texts_unique
__version__ = "0.1.0"

    def test_all_texts_unique(self) -> None:
        texts = [q["text"] for q in AUDIT_QUESTIONS]
        assert len(set(texts)) == 50, "All 50 audit questions must have distinct text"
