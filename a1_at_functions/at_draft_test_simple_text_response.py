# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_simple_text_response.py:7
# Component id: at.source.a1_at_functions.test_simple_text_response
from __future__ import annotations

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
