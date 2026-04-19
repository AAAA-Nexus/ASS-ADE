# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbumpversion.py:15
# Component id: at.source.ass_ade.test_invalid_falls_back_to_initial
__version__ = "0.1.0"

    def test_invalid_falls_back_to_initial(self):
        assert bump_version("not-semver", "patch") == INITIAL_VERSION
