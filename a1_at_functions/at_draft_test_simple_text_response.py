# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:188
# Component id: at.source.ass_ade.test_simple_text_response
__version__ = "0.1.0"

    def test_simple_text_response(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(role="assistant", content="Done."),
                finish_reason="stop",
            )
        ])
        registry = ToolRegistry()
        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
        )
        result = loop.step("Hello")
        assert result == "Done."
