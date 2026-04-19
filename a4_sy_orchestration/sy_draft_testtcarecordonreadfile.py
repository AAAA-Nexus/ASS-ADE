# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:26
# Component id: sy.source.ass_ade.testtcarecordonreadfile
__version__ = "0.1.0"

class TestTCARecordOnReadFile:
    def test_read_file_records_freshness(self, tmp_path):
        target = tmp_path / "example.py"
        target.write_text("x = 1\n")
        server = _make_server(tmp_path)

        result = MagicMock(success=True, output="x = 1\n")
        server._post_tool_hook("read_file", _mk_args(target), result)

        assert server.tca.ncb_contract(target) is True

    def test_read_file_failure_does_not_record(self, tmp_path):
        target = tmp_path / "missing.py"
        server = _make_server(tmp_path)
        result = MagicMock(success=False, error="not found")
        server._post_tool_hook("read_file", _mk_args(target), result)
        assert server.tca.ncb_contract(target) is False
