# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_depth.py:7
# Component id: at.source.a1_at_functions.test_depth
from __future__ import annotations

__version__ = "0.1.0"

def test_depth(self, history: FileHistory):
    assert history.depth("hello.py") == 0
    history.record("hello.py", "v1")
    assert history.depth("hello.py") == 1
    history.record("hello.py", "v2")
    assert history.depth("hello.py") == 2
