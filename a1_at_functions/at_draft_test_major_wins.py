# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testaggregateversion.py:15
# Component id: at.source.ass_ade.test_major_wins
__version__ = "0.1.0"

    def test_major_wins(self):
        assert _aggregate_version(["0.9.9", "1.0.0", "0.9.8"]) == "1.0.0"
