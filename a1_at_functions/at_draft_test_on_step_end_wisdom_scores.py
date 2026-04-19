# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_on_step_end_wisdom_scores.py:7
# Component id: at.source.a1_at_functions.test_on_step_end_wisdom_scores
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_wisdom_scores(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {
        "recon_done": True,
        "atlas_used": True,
        "lifr_queried": True,
        "memory_consulted": True,
        "budget_ok": True,
        "tool_calls": ["read_file"],
    })
    assert report.wisdom_score > 0.0
    assert report.wisdom_passed > 0
