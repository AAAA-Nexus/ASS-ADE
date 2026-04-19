# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:48
# Component id: mo.source.ass_ade.testcontenthash
__version__ = "0.1.0"

class TestContentHash:
    def test_deterministic(self):
        assert content_hash("hello world") == content_hash("hello world")

    def test_different_content(self):
        assert content_hash("foo") != content_hash("bar")

    def test_trailing_whitespace_normalised(self):
        assert content_hash("a  \nb  \n") == content_hash("a\nb")

    def test_returns_16_hex_chars(self):
        h = content_hash("test")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_empty_string(self):
        h = content_hash("")
        assert len(h) == 16
