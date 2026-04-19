# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tool_call_then_response.py:7
# Component id: at.source.a1_at_functions.test_tool_call_then_response
from __future__ import annotations

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
