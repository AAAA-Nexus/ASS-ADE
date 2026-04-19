# Extracted from C:/!ass-ade/tests/test_mcp_gates.py:27
# Component id: sy.source.ass_ade.test_read_file_records_freshness
from __future__ import annotations

__version__ = "0.1.0"

def test_read_file_records_freshness(self, tmp_path):
    target = tmp_path / "example.py"
    target.write_text("x = 1\n")
    server = _make_server(tmp_path)

    result = MagicMock(success=True, output="x = 1\n")
    server._post_tool_hook("read_file", _mk_args(target), result)

    assert server.tca.ncb_contract(target) is True
