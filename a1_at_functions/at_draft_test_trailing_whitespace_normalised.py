# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testcontenthash.py:12
# Component id: at.source.ass_ade.test_trailing_whitespace_normalised
__version__ = "0.1.0"

    def test_trailing_whitespace_normalised(self):
        assert content_hash("a  \nb  \n") == content_hash("a\nb")
