# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:38
# Component id: mo.source.ass_ade.test_ids_are_1_to_50
__version__ = "0.1.0"

    def test_ids_are_1_to_50(self) -> None:
        ids = sorted(q["id"] for q in AUDIT_QUESTIONS)
        assert ids == list(range(1, 51))
