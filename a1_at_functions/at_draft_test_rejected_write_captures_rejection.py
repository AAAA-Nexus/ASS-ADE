# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rejected_write_captures_rejection.py:7
# Component id: at.source.a1_at_functions.test_rejected_write_captures_rejection
from __future__ import annotations

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
