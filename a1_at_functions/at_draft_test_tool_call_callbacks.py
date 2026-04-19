# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tool_call_callbacks.py:7
# Component id: at.source.a1_at_functions.test_tool_call_callbacks
from __future__ import annotations

__version__ = "0.1.0"

def test_tool_call_callbacks(self, tmp_path):
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
            message=Message(role="assistant", content="Done"),
            finish_reason="stop",
        ),
    ])
    registry = ToolRegistry()
    registry.register(_EchoTool())

    calls: list[str] = []

    loop = AgentLoop(
        provider=provider,
        registry=registry,
        working_dir=str(tmp_path),
        on_tool_call=lambda name, args: calls.append(name),
    )
    loop.step("Echo x")
    assert "echo" in calls
