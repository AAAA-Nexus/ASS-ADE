# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testloracaptureonwrite.py:18
# Component id: at.source.ass_ade.test_rejected_write_captures_rejection
__version__ = "0.1.0"

    def test_rejected_write_captures_rejection(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "def bad(:\n    pass\n"}
        server._post_tool_hook("write_file", args, MagicMock(success=True, output="wrote"))
        fly = server.lora_flywheel
        if fly is not None:
            kinds = [c.kind for c in fly._pending]
            assert "rejection" in kinds
