# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateprompt.py:7
# Component id: at.source.a1_at_functions.testvalidateprompt
from __future__ import annotations

__version__ = "0.1.0"

class TestValidatePrompt:
    def test_valid_prompt(self) -> None:
        assert validate_prompt("Hello world") == "Hello world"

    def test_strips_control_chars(self) -> None:
        result = validate_prompt("Hello\x00World\x0b!")
        assert "\x00" not in result
        assert "\x0b" not in result
        assert "HelloWorld!" == result

    def test_preserves_newlines_and_tabs(self) -> None:
        text = "Hello\nWorld\tFoo"
        assert validate_prompt(text) == text

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_prompt("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_prompt("   ")

    def test_oversized_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            validate_prompt("x" * 40_000)
