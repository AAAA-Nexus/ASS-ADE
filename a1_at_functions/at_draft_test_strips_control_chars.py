# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_validation.py:47
# Component id: at.source.ass_ade.test_strips_control_chars
__version__ = "0.1.0"

    def test_strips_control_chars(self) -> None:
        result = validate_prompt("Hello\x00World\x0b!")
        assert "\x00" not in result
        assert "\x0b" not in result
        assert "HelloWorld!" == result
