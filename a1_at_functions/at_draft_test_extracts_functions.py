# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpublicpythonapi.py:6
# Component id: at.source.ass_ade.test_extracts_functions
__version__ = "0.1.0"

    def test_extracts_functions(self):
        body = "def foo(): pass\ndef _bar(): pass\ndef baz(): pass"
        assert _public_python_api(body) == {"foo", "baz"}
