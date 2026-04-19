# Extracted from C:/!ass-ade/tests/test_version_tracker.py:82
# Component id: at.source.ass_ade.test_syntax_error_returns_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_syntax_error_returns_empty(self):
    assert _public_python_api("def (broken") == set()
