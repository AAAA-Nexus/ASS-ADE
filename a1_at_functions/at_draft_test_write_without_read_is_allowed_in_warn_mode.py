# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testncbenforcement.py:6
# Component id: at.source.ass_ade.test_write_without_read_is_allowed_in_warn_mode
__version__ = "0.1.0"

    def test_write_without_read_is_allowed_in_warn_mode(self, tmp_path):
        server = _make_server(tmp_path)
        # Default mode is "warn" → returns (True, "")
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is True
