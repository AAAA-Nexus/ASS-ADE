# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testcontenthash.py:20
# Component id: at.source.ass_ade.test_empty_string
__version__ = "0.1.0"

    def test_empty_string(self):
        h = content_hash("")
        assert len(h) == 16
