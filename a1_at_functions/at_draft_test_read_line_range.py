# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:42
# Component id: at.source.ass_ade.test_read_line_range
from __future__ import annotations

__version__ = "0.1.0"

def test_read_line_range(self, workspace: Path):
    tool = ReadFileTool(str(workspace))
    r = tool.execute(path="sub/data.txt", start_line=2, end_line=2)
    assert r.success
    assert r.output.strip() == "line2"
