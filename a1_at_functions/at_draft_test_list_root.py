# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:130
# Component id: at.source.ass_ade.test_list_root
from __future__ import annotations

__version__ = "0.1.0"

def test_list_root(self, workspace: Path):
    tool = ListDirectoryTool(str(workspace))
    r = tool.execute()
    assert r.success
    assert "hello.py" in r.output
    assert "sub/" in r.output
