# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:71
# Component id: at.source.ass_ade.test_reject_outside_cwd
from __future__ import annotations

__version__ = "0.1.0"

def test_reject_outside_cwd(self, workspace: Path):
    tool = WriteFileTool(str(workspace))
    # Try to escape up
    r = tool.execute(path="../escape.py", content="pwned")
    assert not r.success
    assert "outside" in (r.error or "").lower()
