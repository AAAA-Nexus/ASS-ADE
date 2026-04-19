# Extracted from C:/!ass-ade/tests/test_version_tracker.py:93
# Component id: at.source.ass_ade.test_patch_internal_change
from __future__ import annotations

__version__ = "0.1.0"

def test_patch_internal_change(self):
    old = "def foo():\n    return 1"
    new = "def foo():\n    return 2"
    assert classify_change(old, new) == "patch"
