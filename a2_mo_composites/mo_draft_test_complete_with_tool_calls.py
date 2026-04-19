# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:103
# Component id: mo.source.ass_ade.test_complete_with_tool_calls
__version__ = "0.1.0"

    def test_complete_with_tool_calls(self, mock_client_cls):
        raw_tool_calls = [
            {
                "id": "call_1",
                "type": "function",
                "function": {
                    "name": "read_file",
                    "arguments": json.dumps({"path": "main.py"}),
                },
            }
        ]
        mock_resp = MagicMock()
        mock_resp.json.return_value = self._mock_response(content="", tool_calls=raw_tool_calls)
        mock_resp.raise_for_status = MagicMock()

        mock_instance = MagicMock()
        mock_instance.post.return_value = mock_resp
        mock_client_cls.return_value = mock_instance

        provider = OpenAICompatibleProvider(base_url="http://test:8000/v1", api_key="k")
        req = CompletionRequest(
            messages=[Message(role="user", content="read main.py")],
            tools=[ToolSchema(name="read_file", description="Read file", parameters={"type": "object"})],
        )
        resp = provider.complete(req)

        assert len(resp.message.tool_calls) == 1
        assert resp.message.tool_calls[0].name == "read_file"
        assert resp.message.tool_calls[0].arguments == {"path": "main.py"}
