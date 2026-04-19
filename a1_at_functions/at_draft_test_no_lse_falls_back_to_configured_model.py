# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_no_lse_falls_back_to_configured_model.py:7
# Component id: at.source.a1_at_functions.test_no_lse_falls_back_to_configured_model
from __future__ import annotations

__version__ = "0.1.0"

def test_no_lse_falls_back_to_configured_model(self):
    provider = _make_provider_returning_text("ok")
    registry = ToolRegistry()
    loop = AgentLoop(
        provider=provider,
        registry=registry,
        model="claude-sonnet-4-6",
    )
    loop.step("any")
    call_args = provider.complete.call_args
    request = call_args[0][0] if call_args[0] else call_args[1].get("request")
    assert request.model == "claude-sonnet-4-6"
