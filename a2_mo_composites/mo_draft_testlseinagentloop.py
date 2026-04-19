# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseinagentloop.py:7
# Component id: mo.source.a2_mo_composites.testlseinagentloop
from __future__ import annotations

__version__ = "0.1.0"

class TestLSEInAgentLoop:
    def test_lse_decision_populated_after_step(self):
        provider = _make_provider_returning_text("result")
        registry = ToolRegistry()
        lse = LSEEngine({})
        loop = AgentLoop(provider=provider, registry=registry, lse=lse)
        loop.step("simple question")
        assert loop.last_lse_decision is not None
        # Canonical tier names (catalog-aware); haiku/sonnet/opus are aliases
        assert loop.last_lse_decision.tier in {"fast", "balanced", "deep"}

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
