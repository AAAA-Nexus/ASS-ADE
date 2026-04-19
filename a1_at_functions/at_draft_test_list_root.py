# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_list_root.py:7
# Component id: at.source.a1_at_functions.test_list_root
from __future__ import annotations

__version__ = "0.1.0"

def test_list_root(self, workspace: Path):
    tool = ListDirectoryTool(str(workspace))
    r = tool.execute()
    assert r.success
    assert "hello.py" in r.output
    assert "sub/" in r.output
