# Extracted from C:/!ass-ade/tests/test_agent.py:204
# Component id: at.source.ass_ade.test_whitespace_only_text_response_is_preserved
from __future__ import annotations

__version__ = "0.1.0"

def test_whitespace_only_text_response_is_preserved(self, tmp_path):
    provider = _MockProvider([
        CompletionResponse(
            message=Message(role="assistant", content="   "),
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
    assert result == "   "
