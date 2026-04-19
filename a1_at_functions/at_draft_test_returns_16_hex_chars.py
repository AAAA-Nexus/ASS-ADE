# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testcontenthash.py:15
# Component id: at.source.ass_ade.test_returns_16_hex_chars
__version__ = "0.1.0"

    def test_returns_16_hex_chars(self):
        h = content_hash("test")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)
