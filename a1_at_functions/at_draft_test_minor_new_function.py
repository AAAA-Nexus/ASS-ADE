# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_minor_new_function.py:7
# Component id: at.source.a1_at_functions.test_minor_new_function
from __future__ import annotations

__version__ = "0.1.0"

def test_minor_new_function(self):
    old = "def foo(): pass"
    new = "def foo(): pass\ndef bar(): pass"
    assert classify_change(old, new) == "minor"
