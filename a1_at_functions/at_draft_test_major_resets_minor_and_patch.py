# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbumpversion.py:21
# Component id: at.source.ass_ade.test_major_resets_minor_and_patch
__version__ = "0.1.0"

    def test_major_resets_minor_and_patch(self):
        assert bump_version("2.5.7", "major") == "3.0.0"
