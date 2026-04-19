# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_teststepstream.py:6
# Component id: at.source.ass_ade.test_simple_done_event
__version__ = "0.1.0"

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
