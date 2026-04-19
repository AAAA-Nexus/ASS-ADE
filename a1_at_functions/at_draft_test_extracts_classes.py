# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpublicpythonapi.py:10
# Component id: at.source.ass_ade.test_extracts_classes
__version__ = "0.1.0"

    def test_extracts_classes(self):
        body = "class Foo: pass\nclass _Hidden: pass"
        assert _public_python_api(body) == {"Foo"}
