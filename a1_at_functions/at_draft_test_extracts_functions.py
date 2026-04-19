# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_extracts_functions.py:7
# Component id: at.source.a1_at_functions.test_extracts_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_extracts_functions(self):
    body = "def foo(): pass\ndef _bar(): pass\ndef baz(): pass"
    assert _public_python_api(body) == {"foo", "baz"}
