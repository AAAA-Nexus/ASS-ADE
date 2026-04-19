# Extracted from C:/!ass-ade/tests/test_mcp_server_streaming.py:181
# Component id: sy.source.ass_ade.test_apply_includes_diff
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_includes_diff(self, tmp_path: Path):
    (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
    tool = EditFileTool(str(tmp_path))
    result = tool.execute(
        path="code.py",
        old_string="y = 2",
        new_string="y = 42",
        preview=False,
    )
    assert result.success
    assert "Applied edit" in result.output
    assert "-y = 2" in result.output
    assert "+y = 42" in result.output
    # File should be changed
    assert "y = 42" in (tmp_path / "code.py").read_text()
