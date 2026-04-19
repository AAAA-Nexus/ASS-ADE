# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testgrepsearch.py:6
# Component id: at.source.ass_ade.test_find_pattern
__version__ = "0.1.0"

    def test_find_pattern(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="hello")
        assert r.success
        assert "hello.py" in r.output
