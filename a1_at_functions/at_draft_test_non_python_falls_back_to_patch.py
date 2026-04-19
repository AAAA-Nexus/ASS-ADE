# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_non_python_falls_back_to_patch.py:7
# Component id: at.source.a1_at_functions.test_non_python_falls_back_to_patch
from __future__ import annotations

__version__ = "0.1.0"

def test_non_python_falls_back_to_patch(self):
    assert classify_change("old code", "new code", language="rust") == "patch"
