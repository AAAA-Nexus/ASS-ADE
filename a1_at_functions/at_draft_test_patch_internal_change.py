# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifychange.py:10
# Component id: at.source.ass_ade.test_patch_internal_change
__version__ = "0.1.0"

    def test_patch_internal_change(self):
        old = "def foo():\n    return 1"
        new = "def foo():\n    return 2"
        assert classify_change(old, new) == "patch"
