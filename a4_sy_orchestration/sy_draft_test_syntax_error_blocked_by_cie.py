# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:96
# Component id: sy.source.ass_ade.test_syntax_error_blocked_by_cie
__version__ = "0.1.0"

    def test_syntax_error_blocked_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        target = tmp_path / "broken.py"
        # Pre-write so undo_edit has something to roll back (not strictly needed here)
        target.write_text("")
        args = {"path": str(target), "content": "def broken(:\n    pass\n"}
        original = MagicMock(success=True, output="wrote")
        out = server._post_tool_hook("write_file", args, original)
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")
