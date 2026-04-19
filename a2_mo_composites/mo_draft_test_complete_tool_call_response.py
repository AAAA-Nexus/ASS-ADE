# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:154
# Component id: mo.source.ass_ade.test_complete_tool_call_response
__version__ = "0.1.0"

    def test_complete_tool_call_response(self):
        tool_json = json.dumps({"tool_call": {"name": "read_file", "arguments": {"path": "x.py"}}})
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result=tool_json,
            text=None,
            model="llama-3.1-8b",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(
            messages=[Message(role="user", content="read x.py")],
            tools=[ToolSchema(name="read_file", description="Read file", parameters={"type": "object"})],
        )
        resp = provider.complete(req)

        assert len(resp.message.tool_calls) == 1
        assert resp.message.tool_calls[0].name == "read_file"
        assert resp.finish_reason == "tool_calls"
