# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:148
# Component id: at.source.ass_ade.test_glob_py
from __future__ import annotations

__version__ = "0.1.0"

def test_glob_py(self, workspace: Path):
    tool = SearchFilesTool(str(workspace))
    r = tool.execute(pattern="**/*.py")
    assert r.success
    assert "hello.py" in r.output
