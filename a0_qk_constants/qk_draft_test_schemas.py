# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tools_builtin.py:203
# Component id: qk.source.ass_ade.test_schemas
__version__ = "0.1.0"

    def test_schemas(self, workspace: Path):
        reg = default_registry(str(workspace))
        schemas = reg.schemas()
        assert len(schemas) == len(reg.list_tools())
        assert all(s.name for s in schemas)
