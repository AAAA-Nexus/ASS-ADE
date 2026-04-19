# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpublicpythonapi.py:5
# Component id: mo.source.ass_ade.testpublicpythonapi
__version__ = "0.1.0"

class TestPublicPythonApi:
    def test_extracts_functions(self):
        body = "def foo(): pass\ndef _bar(): pass\ndef baz(): pass"
        assert _public_python_api(body) == {"foo", "baz"}

    def test_extracts_classes(self):
        body = "class Foo: pass\nclass _Hidden: pass"
        assert _public_python_api(body) == {"Foo"}

    def test_empty_body(self):
        assert _public_python_api("") == set()

    def test_syntax_error_returns_empty(self):
        assert _public_python_api("def (broken") == set()
