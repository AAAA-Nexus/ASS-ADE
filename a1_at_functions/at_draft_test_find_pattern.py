# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:164
# Component id: at.source.ass_ade.test_find_pattern
from __future__ import annotations

__version__ = "0.1.0"

def test_find_pattern(self, workspace: Path):
    tool = GrepSearchTool(str(workspace))
    r = tool.execute(pattern="hello")
    assert r.success
    assert "hello.py" in r.output
