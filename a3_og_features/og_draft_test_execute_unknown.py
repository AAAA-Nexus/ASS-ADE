# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testregistry.py:17
# Component id: og.source.ass_ade.test_execute_unknown
__version__ = "0.1.0"

    def test_execute_unknown(self, workspace: Path):
        reg = default_registry(str(workspace))
        r = reg.execute("no_such_tool")
        assert not r.success
        assert "Unknown tool" in (r.error or "")
