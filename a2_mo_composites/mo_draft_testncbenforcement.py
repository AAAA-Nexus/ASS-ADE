# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testncbenforcement.py:5
# Component id: mo.source.ass_ade.testncbenforcement
__version__ = "0.1.0"

class TestNCBEnforcement:
    def test_write_without_read_is_allowed_in_warn_mode(self, tmp_path):
        server = _make_server(tmp_path)
        # Default mode is "warn" → returns (True, "")
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is True

    def test_write_without_read_is_blocked_in_block_mode(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is False
        assert "NCB violation" in reason

    def test_write_after_read_is_allowed_in_block_mode(self, tmp_path):
        target = tmp_path / "existing.py"
        target.write_text("y = 2\n")
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        # Record a read
        server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="y = 2\n"))
        allow, reason = server._pre_tool_hook("write_file", _mk_args(target))
        assert allow is True

    def test_ncb_check_skipped_for_non_write_tools(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        # list_directory etc. should never be NCB-gated
        allow, _ = server._pre_tool_hook("list_directory", _mk_args(tmp_path))
        assert allow is True
