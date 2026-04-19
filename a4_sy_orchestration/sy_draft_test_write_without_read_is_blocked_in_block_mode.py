# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:57
# Component id: sy.source.ass_ade.test_write_without_read_is_blocked_in_block_mode
__version__ = "0.1.0"

    def test_write_without_read_is_blocked_in_block_mode(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is False
        assert "NCB violation" in reason
