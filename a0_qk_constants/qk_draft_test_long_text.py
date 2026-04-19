# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatetokens.py:20
# Component id: qk.source.ass_ade.test_long_text
__version__ = "0.1.0"

    def test_long_text(self):
        text = "The quick brown fox jumps over the lazy dog. " * 100
        result = estimate_tokens(text)
        # ~4500 chars / 3.7 ≈ ~1216 tokens
        assert 800 < result < 2000
