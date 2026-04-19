# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testgrepsearch.py:17
# Component id: at.source.ass_ade.test_invalid_regex
__version__ = "0.1.0"

    def test_invalid_regex(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="[invalid")
        assert not r.success
        assert "Invalid regex" in (r.error or "")
