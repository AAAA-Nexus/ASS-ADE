# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testgrepsearch.py:12
# Component id: at.source.ass_ade.test_no_matches
__version__ = "0.1.0"

    def test_no_matches(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="ZZZZZ_NOTHING")
        assert "No matches" in r.output
