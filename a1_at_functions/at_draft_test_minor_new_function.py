# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifychange.py:15
# Component id: at.source.ass_ade.test_minor_new_function
__version__ = "0.1.0"

    def test_minor_new_function(self):
        old = "def foo(): pass"
        new = "def foo(): pass\ndef bar(): pass"
        assert classify_change(old, new) == "minor"
