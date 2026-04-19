# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:18
# Component id: at.source.ass_ade.test_depth
__version__ = "0.1.0"

    def test_depth(self, history: FileHistory):
        assert history.depth("hello.py") == 0
        history.record("hello.py", "v1")
        assert history.depth("hello.py") == 1
        history.record("hello.py", "v2")
        assert history.depth("hello.py") == 2
