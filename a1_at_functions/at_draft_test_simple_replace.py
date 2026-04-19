# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditfile.py:6
# Component id: at.source.ass_ade.test_simple_replace
__version__ = "0.1.0"

    def test_simple_replace(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="hello world", new_string="goodbye world")
        assert r.success
        assert (workspace / "hello.py").read_text() == "print('goodbye world')\n"
