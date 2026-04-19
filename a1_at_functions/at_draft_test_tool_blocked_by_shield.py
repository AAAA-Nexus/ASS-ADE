# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tool_blocked_by_shield.py:7
# Component id: at.source.a1_at_functions.test_tool_blocked_by_shield
from __future__ import annotations

__version__ = "0.1.0"

def test_tool_blocked_by_shield(self, tmp_path):
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
            message=Message(role="assistant", content="Tool was blocked."),
            finish_reason="stop",
        ),
    ])
    registry = ToolRegistry()
    registry.register(_EchoTool())

    mock_gates = MagicMock(spec=QualityGates)
    mock_gates.scan_prompt.return_value = {"blocked": False}
    mock_gates.shield_tool.return_value = {"blocked": True, "reason": "dangerous"}
    mock_gates.check_hallucination.return_value = None

    loop = AgentLoop(
        provider=provider,
        registry=registry,
        working_dir=str(tmp_path),
        quality_gates=mock_gates,
    )
    result = loop.step("Do something dangerous")
    # The model should see the blocked error and respond
    assert "blocked" in result.lower() or "Tool was blocked" in result
