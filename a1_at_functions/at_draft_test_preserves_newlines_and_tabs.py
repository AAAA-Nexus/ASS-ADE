# Extracted from C:/!ass-ade/tests/test_validation.py:53
# Component id: at.source.ass_ade.test_preserves_newlines_and_tabs
from __future__ import annotations

__version__ = "0.1.0"

def test_preserves_newlines_and_tabs(self) -> None:
    text = "Hello\nWorld\tFoo"
    assert validate_prompt(text) == text
