# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateprompt.py:11
# Component id: at.source.a1_at_functions.test_strips_control_chars
from __future__ import annotations

__version__ = "0.1.0"

def test_strips_control_chars(self) -> None:
    result = validate_prompt("Hello\x00World\x0b!")
    assert "\x00" not in result
    assert "\x0b" not in result
    assert "HelloWorld!" == result
