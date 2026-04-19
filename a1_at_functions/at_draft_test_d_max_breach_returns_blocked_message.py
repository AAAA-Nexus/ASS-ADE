# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:162
# Component id: at.source.ass_ade.test_d_max_breach_returns_blocked_message
from __future__ import annotations

__version__ = "0.1.0"

def test_d_max_breach_returns_blocked_message(self):
    provider = _make_provider_returning_text("ok")
    registry = ToolRegistry()
    orchestrator = EngineOrchestrator({})
    loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

    # Simulate being inside a recursion by setting depth past D_MAX
    loop._delegation_depth = D_MAX + 1
    result = loop.step("[REFINE round 1/3] retry")
    assert "D_MAX" in result or "delegation" in result.lower()
