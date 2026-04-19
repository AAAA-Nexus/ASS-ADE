# Extracted from C:/!ass-ade/tests/test_agent.py:250
# Component id: at.source.ass_ade.test_tool_call_callbacks
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
