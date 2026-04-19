# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:34
# Component id: mo.source.ass_ade.test_all_texts_unique
__version__ = "0.1.0"

    def test_all_texts_unique(self) -> None:
        texts = [q["text"] for q in AUDIT_QUESTIONS]
        assert len(set(texts)) == 50, "All 50 audit questions must have distinct text"
