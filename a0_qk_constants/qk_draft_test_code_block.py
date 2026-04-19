# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatetokens.py:14
# Component id: qk.source.ass_ade.test_code_block
__version__ = "0.1.0"

    def test_code_block(self):
        code = "def fibonacci(n: int) -> int:\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n"
        result = estimate_tokens(code)
        assert result >= 10
        assert result <= 100
