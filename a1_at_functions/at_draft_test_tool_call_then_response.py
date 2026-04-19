# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:220
# Component id: at.source.ass_ade.test_tool_call_then_response
__version__ = "0.1.0"

    def test_tool_call_then_response(self, tmp_path):
        provider = _MockProvider([
            # First call: model requests a tool call
            CompletionResponse(
                message=Message(
                    role="assistant",
                    content="",
                    tool_calls=[
                        ToolCallRequest(id="c1", name="echo", arguments={"text": "ping"})
                    ],
                ),
                finish_reason="tool_calls",
            ),
            # Second call: model returns final text
            CompletionResponse(
                message=Message(role="assistant", content="Got: echoed: ping"),
                finish_reason="stop",
            ),
        ])
        registry = ToolRegistry()
        registry.register(_EchoTool())

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
        )
        result = loop.step("Echo ping")
        assert "echoed: ping" in result
