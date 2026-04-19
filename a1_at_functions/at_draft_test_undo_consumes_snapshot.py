# Extracted from C:/!ass-ade/tests/test_history.py:61
# Component id: at.source.ass_ade.test_undo_consumes_snapshot
from __future__ import annotations

__version__ = "0.1.0"

def test_undo_consumes_snapshot(self, history: FileHistory, tmp_workspace: Path):
    history.record("hello.py", "v1")
    history.record("hello.py", "v2")
    assert history.depth("hello.py") == 2

    history.undo("hello.py")
    assert history.depth("hello.py") == 1
