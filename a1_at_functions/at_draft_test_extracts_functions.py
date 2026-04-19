# Extracted from C:/!ass-ade/tests/test_version_tracker.py:71
# Component id: at.source.ass_ade.test_extracts_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_extracts_functions(self):
    body = "def foo(): pass\ndef _bar(): pass\ndef baz(): pass"
    assert _public_python_api(body) == {"foo", "baz"}
