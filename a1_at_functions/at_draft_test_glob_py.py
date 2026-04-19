# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testsearchfiles.py:8
# Component id: at.source.a2_mo_composites.test_glob_py
from __future__ import annotations

__version__ = "0.1.0"

def test_glob_py(self, workspace: Path):
    tool = SearchFilesTool(str(workspace))
    r = tool.execute(pattern="**/*.py")
    assert r.success
    assert "hello.py" in r.output
