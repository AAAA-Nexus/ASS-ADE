# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_blocked_event.py:7
# Component id: at.source.a1_at_functions.test_blocked_event
from __future__ import annotations

__version__ = "0.1.0"

def test_blocked_event(self, tmp_path):
    provider = _MockProvider([])
    mock_gates = MagicMock()
    mock_gates.scan_prompt.return_value = {"blocked": True}

    loop = AgentLoop(
        provider=provider,
        registry=ToolRegistry(),
        working_dir=str(tmp_path),
        quality_gates=mock_gates,
    )
    events = list(loop.step_stream("Bad input"))
    assert len(events) == 1
    assert events[0].kind == "blocked"
