# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_patch_internal_change.py:7
# Component id: at.source.a1_at_functions.test_patch_internal_change
from __future__ import annotations

__version__ = "0.1.0"

def test_patch_internal_change(self):
    old = "def foo():\n    return 1"
    new = "def foo():\n    return 2"
    assert classify_change(old, new) == "patch"
