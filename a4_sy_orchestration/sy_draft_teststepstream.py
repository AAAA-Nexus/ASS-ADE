# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:231
# Component id: sy.source.ass_ade.teststepstream
__version__ = "0.1.0"

class TestStepStream:
    def test_simple_done_event(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(role="assistant", content="Hello!"),
                finish_reason="stop",
            )
        ])
        loop = AgentLoop(
            provider=provider,
            registry=ToolRegistry(),
            working_dir=str(tmp_path),
        )
        events = list(loop.step_stream("Hi"))
        assert len(events) == 1
        assert events[0].kind == "done"
        assert events[0].text == "Hello!"

    def test_tool_call_events(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(
                    role="assistant",
                    content="",
                    tool_calls=[
                        ToolCallRequest(id="c1", name="echo", arguments={"text": "x"})
                    ],
                ),
                finish_reason="tool_calls",
            ),
            CompletionResponse(
                message=Message(role="assistant", content="Done."),
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
        events = list(loop.step_stream("Echo x"))

        kinds = [e.kind for e in events]
        assert "tool_call" in kinds
        assert "tool_result" in kinds
        assert "done" in kinds

        tool_event = next(e for e in events if e.kind == "tool_call")
        assert tool_event.tool_name == "echo"

        result_event = next(e for e in events if e.kind == "tool_result")
        assert result_event.tool_result is not None
        assert result_event.tool_result.success

    def test_blocked_event(self, tmp_path):
        provider = _MockProvider([])
        mock_gates = MagicMock()
        mock_gates.scan_prompt.return_value = {"blocked": True}

        loop = AgentLoop(
            provider=provider,
            registry=ToolRegistry(),
            working_dir=str(tmp_path),
            quality_gates=mock_gates,
        )
        events = list(loop.step_stream("Bad input"))
        assert len(events) == 1
        assert events[0].kind == "blocked"

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
