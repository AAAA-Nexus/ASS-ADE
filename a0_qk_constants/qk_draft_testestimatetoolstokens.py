# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatetoolstokens.py:5
# Component id: qk.source.ass_ade.testestimatetoolstokens
__version__ = "0.1.0"

class TestEstimateToolsTokens:
    def test_empty_list(self):
        assert estimate_tools_tokens([]) == 0

    def test_single_tool(self):
        tool = ToolSchema(
            name="read_file",
            description="Read a file",
            parameters={"type": "object", "properties": {"path": {"type": "string"}}},
        )
        tokens = estimate_tools_tokens([tool])
        assert tokens > 0

    def test_multiple_tools(self):
        tools = [
            ToolSchema(name=f"tool_{i}", description=f"Tool number {i}", parameters={"type": "object"})
            for i in range(5)
        ]
        tokens = estimate_tools_tokens(tools)
        assert tokens > estimate_tools_tokens(tools[:1])
