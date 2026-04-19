# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:44
# Component id: qk.source.ass_ade.testtoolschema
__version__ = "0.1.0"

class TestToolSchema:
    def test_schema(self):
        s = ToolSchema(name="read_file", description="Read a file", parameters={"type": "object"})
        assert s.name == "read_file"
