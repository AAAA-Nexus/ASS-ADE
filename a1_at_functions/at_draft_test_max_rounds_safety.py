# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:281
# Component id: at.source.ass_ade.test_max_rounds_safety
__version__ = "0.1.0"

    def test_max_rounds_safety(self, tmp_path):
        """If model keeps calling tools forever, loop terminates."""
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
        result = loop.step("Loop forever")
        assert result == MAX_ROUNDS_SENTINEL
