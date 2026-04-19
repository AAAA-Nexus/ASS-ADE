# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditfile.py:5
# Component id: mo.source.ass_ade.testeditfile
__version__ = "0.1.0"

class TestEditFile:
    def test_simple_replace(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="hello world", new_string="goodbye world")
        assert r.success
        assert (workspace / "hello.py").read_text() == "print('goodbye world')\n"

    def test_not_found(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="NOPE", new_string="X")
        assert not r.success
        assert "not found" in (r.error or "").lower()

    def test_multiple_matches(self, workspace: Path):
        (workspace / "dup.py").write_text("a\na\na\n", encoding="utf-8")
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="dup.py", old_string="a", new_string="b")
        assert not r.success
        assert "3 locations" in (r.error or "")
