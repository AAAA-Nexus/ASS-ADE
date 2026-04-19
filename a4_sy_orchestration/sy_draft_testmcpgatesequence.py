# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:167
# Component id: sy.source.ass_ade.testmcpgatesequence
__version__ = "0.1.0"

class TestMCPGateSequence:
    def test_read_then_write_passes_all_gates(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        target = tmp_path / "app.py"
        target.write_text("x = 1\n")

        # 1. read_file → TCA records freshness
        server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="x = 1\n"))
        # 2. write_file pre-check → NCB passes (we just read it)
        allow, _ = server._pre_tool_hook("write_file", _mk_args(target))
        assert allow is True
        # 3. write_file post-check → CIE accepts clean code
        new_code = "def run():\n    return 2\n"
        out = server._post_tool_hook(
            "write_file",
            {"path": str(target), "content": new_code},
            MagicMock(success=True, output="wrote"),
        )
        assert out.success is True

    def test_write_without_read_blocked_end_to_end(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        target = tmp_path / "never_read.py"
        allow, reason = server._pre_tool_hook("write_file", _mk_args(target, content="def x(): pass"))
        assert allow is False
        assert "NCB" in reason
