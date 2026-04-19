# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testloracaptureonwrite.py:6
# Component id: at.source.ass_ade.test_accepted_write_captures_fix
__version__ = "0.1.0"

    def test_accepted_write_captures_fix(self, tmp_path, monkeypatch):
        # Isolate LoRA state to tmp_path
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "module.py"), "content": "def g(): return 42\n"}
        server._post_tool_hook("write_file", args, MagicMock(success=True, output="wrote"))
        # Flywheel should have 1 captured fix
        fly = server.lora_flywheel
        if fly is not None:
            kinds = [c.kind for c in fly._pending]
            assert "fix" in kinds
