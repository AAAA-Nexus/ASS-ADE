# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:37
# Component id: sy.source.ass_ade.test_read_file_failure_does_not_record
__version__ = "0.1.0"

    def test_read_file_failure_does_not_record(self, tmp_path):
        target = tmp_path / "missing.py"
        server = _make_server(tmp_path)
        result = MagicMock(success=False, error="not found")
        server._post_tool_hook("read_file", _mk_args(target), result)
        assert server.tca.ncb_contract(target) is False
