# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateprompt.py:15
# Component id: at.source.ass_ade.test_preserves_newlines_and_tabs
__version__ = "0.1.0"

    def test_preserves_newlines_and_tabs(self) -> None:
        text = "Hello\nWorld\tFoo"
        assert validate_prompt(text) == text
