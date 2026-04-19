# Extracted from C:/!ass-ade/tests/test_mcp_gates.py:64
# Component id: sy.source.ass_ade.test_write_after_read_is_allowed_in_block_mode
from __future__ import annotations

__version__ = "0.1.0"

def test_write_after_read_is_allowed_in_block_mode(self, tmp_path):
    target = tmp_path / "existing.py"
    target.write_text("y = 2\n")
    server = _make_server(tmp_path)
    server._ncb_mode = "block"
    # Record a read
    server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="y = 2\n"))
    allow, reason = server._pre_tool_hook("write_file", _mk_args(target))
    assert allow is True
