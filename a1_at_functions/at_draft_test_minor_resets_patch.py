# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbumpversion.py:18
# Component id: at.source.ass_ade.test_minor_resets_patch
__version__ = "0.1.0"

    def test_minor_resets_patch(self):
        assert bump_version("1.2.9", "minor") == "1.3.0"
