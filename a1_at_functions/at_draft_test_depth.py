# Extracted from C:/!ass-ade/tests/test_history.py:38
# Component id: at.source.ass_ade.test_depth
from __future__ import annotations

__version__ = "0.1.0"

def test_depth(self, history: FileHistory):
    assert history.depth("hello.py") == 0
    history.record("hello.py", "v1")
    assert history.depth("hello.py") == 1
    history.record("hello.py", "v2")
    assert history.depth("hello.py") == 2
