# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpublicpythonapi.py:17
# Component id: at.source.ass_ade.test_syntax_error_returns_empty
__version__ = "0.1.0"

    def test_syntax_error_returns_empty(self):
        assert _public_python_api("def (broken") == set()
