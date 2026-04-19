# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testciegateonwrite.py:41
# Component id: at.source.ass_ade.test_failed_write_is_not_cie_gated
__version__ = "0.1.0"

    def test_failed_write_is_not_cie_gated(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "x.py"), "content": "def ok(): pass"}
        result = MagicMock(success=False, error="disk full")
        out = server._post_tool_hook("write_file", args, result)
        # Unchanged — CIE only runs on successful writes
        assert out.success is False
        assert out.error == "disk full"
