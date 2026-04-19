# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifychange.py:6
# Component id: at.source.ass_ade.test_identical
__version__ = "0.1.0"

    def test_identical(self):
        body = "def foo(): pass"
        assert classify_change(body, body) == "none"
