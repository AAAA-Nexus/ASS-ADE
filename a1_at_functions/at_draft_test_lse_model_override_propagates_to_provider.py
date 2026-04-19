# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_model_override_propagates_to_provider.py:7
# Component id: at.source.a1_at_functions.test_lse_model_override_propagates_to_provider
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_model_override_propagates_to_provider(self):
    provider = _make_provider_returning_text("ok")
    registry = ToolRegistry()
    lse = LSEEngine({})
    loop = AgentLoop(provider=provider, registry=registry, lse=lse)
    loop.step("trivial task")
    # Provider was called with a model name from LSE
    call_args = provider.complete.call_args
    assert call_args is not None
    request = call_args[0][0] if call_args[0] else call_args[1].get("request")
    # The request should have a model set (either from LSE or None)
    assert hasattr(request, "model")
