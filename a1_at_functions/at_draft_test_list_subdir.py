# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:137
# Component id: at.source.ass_ade.test_list_subdir
from __future__ import annotations

__version__ = "0.1.0"

def test_list_subdir(self, workspace: Path):
    tool = ListDirectoryTool(str(workspace))
    r = tool.execute(path="sub")
    assert r.success
    assert "data.txt" in r.output
