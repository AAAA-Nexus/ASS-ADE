# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testncbenforcement.py:29
# Component id: at.source.ass_ade.test_ncb_check_skipped_for_non_write_tools
__version__ = "0.1.0"

    def test_ncb_check_skipped_for_non_write_tools(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        # list_directory etc. should never be NCB-gated
        allow, _ = server._pre_tool_hook("list_directory", _mk_args(tmp_path))
        assert allow is True
