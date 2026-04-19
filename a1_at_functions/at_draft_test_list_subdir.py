# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_list_subdir.py:7
# Component id: at.source.a1_at_functions.test_list_subdir
from __future__ import annotations

__version__ = "0.1.0"

def test_list_subdir(self, workspace: Path):
    tool = ListDirectoryTool(str(workspace))
    r = tool.execute(path="sub")
    assert r.success
    assert "data.txt" in r.output
