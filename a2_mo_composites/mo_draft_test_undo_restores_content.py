# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:25
# Component id: mo.source.ass_ade.test_undo_restores_content
__version__ = "0.1.0"

    def test_undo_restores_content(self, history: FileHistory, tmp_workspace: Path):
        original = "print('hello')\n"
        history.record("hello.py", original)

        # Overwrite the file
        (tmp_workspace / "hello.py").write_text("print('goodbye')\n", encoding="utf-8")

        # Undo should restore
        snap = history.undo("hello.py")
        assert snap is not None
        assert snap.content == original
        assert (tmp_workspace / "hello.py").read_text(encoding="utf-8") == original
