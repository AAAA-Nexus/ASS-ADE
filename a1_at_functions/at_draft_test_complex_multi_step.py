# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifycomplexity.py:14
# Component id: at.source.ass_ade.test_complex_multi_step
__version__ = "0.1.0"

    def test_complex_multi_step(self):
        c = classify_complexity(
            "First, implement a REST API endpoint for user registration, "
            "then write integration tests and create a database migration"
        )
        assert c >= 0.5
