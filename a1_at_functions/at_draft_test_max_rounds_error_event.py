# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_max_rounds_error_event.py:7
# Component id: at.source.a1_at_functions.test_max_rounds_error_event
from __future__ import annotations

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
