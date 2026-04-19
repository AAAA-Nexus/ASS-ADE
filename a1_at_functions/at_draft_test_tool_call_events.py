# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tool_call_events.py:7
# Component id: at.source.a1_at_functions.test_tool_call_events
from __future__ import annotations

__version__ = "0.1.0"

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
