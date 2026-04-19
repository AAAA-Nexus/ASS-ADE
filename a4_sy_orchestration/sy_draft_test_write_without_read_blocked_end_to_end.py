# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpgatesequence.py:29
# Component id: sy.source.a4_sy_orchestration.test_write_without_read_blocked_end_to_end
from __future__ import annotations

__version__ = "0.1.0"

def test_write_without_read_blocked_end_to_end(self, tmp_path):
    server = _make_server(tmp_path)
    server._ncb_mode = "block"
    target = tmp_path / "never_read.py"
    allow, reason = server._pre_tool_hook("write_file", _mk_args(target, content="def x(): pass"))
    assert allow is False
    assert "NCB" in reason
