# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testloracaptureonwrite.py:7
# Component id: mo.source.a2_mo_composites.testloracaptureonwrite
from __future__ import annotations

__version__ = "0.1.0"

class TestLoRACaptureOnWrite:
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

    def test_rejected_write_captures_rejection(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "def bad(:\n    pass\n"}
        server._post_tool_hook("write_file", args, MagicMock(success=True, output="wrote"))
        fly = server.lora_flywheel
        if fly is not None:
            kinds = [c.kind for c in fly._pending]
            assert "rejection" in kinds
