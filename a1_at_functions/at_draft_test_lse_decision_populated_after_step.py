# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_decision_populated_after_step.py:7
# Component id: at.source.a1_at_functions.test_lse_decision_populated_after_step
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_decision_populated_after_step(self):
    provider = _make_provider_returning_text("result")
    registry = ToolRegistry()
    lse = LSEEngine({})
    loop = AgentLoop(provider=provider, registry=registry, lse=lse)
    loop.step("simple question")
    assert loop.last_lse_decision is not None
    # Canonical tier names (catalog-aware); haiku/sonnet/opus are aliases
    assert loop.last_lse_decision.tier in {"fast", "balanced", "deep"}
