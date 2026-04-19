# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_sam_result_none_when_no_gates.py:7
# Component id: at.source.a1_at_functions.test_sam_result_none_when_no_gates
from __future__ import annotations

__version__ = "0.1.0"

def test_sam_result_none_when_no_gates(self):
    provider = _make_provider_returning_text("hello")
    registry = ToolRegistry()
    loop = AgentLoop(provider=provider, registry=registry)
    loop.step("What is 2+2?")
    assert loop.last_sam_result is None
