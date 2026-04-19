# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateprompt.py:17
# Component id: at.source.a1_at_functions.test_preserves_newlines_and_tabs
from __future__ import annotations

__version__ = "0.1.0"

def test_preserves_newlines_and_tabs(self) -> None:
    text = "Hello\nWorld\tFoo"
    assert validate_prompt(text) == text
