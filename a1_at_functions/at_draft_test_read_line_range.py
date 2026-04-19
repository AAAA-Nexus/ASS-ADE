# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_read_line_range.py:7
# Component id: at.source.a1_at_functions.test_read_line_range
from __future__ import annotations

__version__ = "0.1.0"

def test_read_line_range(self, workspace: Path):
    tool = ReadFileTool(str(workspace))
    r = tool.execute(path="sub/data.txt", start_line=2, end_line=2)
    assert r.success
    assert r.output.strip() == "line2"
