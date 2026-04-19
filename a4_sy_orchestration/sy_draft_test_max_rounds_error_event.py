# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:303
# Component id: sy.source.ass_ade.test_max_rounds_error_event
__version__ = "0.1.0"

    def test_max_rounds_error_event(self, tmp_path):
        never_stop = CompletionResponse(
            message=Message(
                role="assistant",
                content="",
                tool_calls=[
                    ToolCallRequest(id="c1", name="echo", arguments={"text": "loop"})
                ],
            ),
            finish_reason="tool_calls",
        )
        provider = _MockProvider([never_stop] * 30)
        registry = ToolRegistry()
        registry.register(_EchoTool())

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
        )
        events = list(loop.step_stream("Loop"))
        assert events[-1].kind == "error"
        assert "maximum" in events[-1].text.lower()
