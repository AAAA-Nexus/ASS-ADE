# Extracted from C:/!ass-ade/tests/test_mcp_server_streaming.py:288
# Component id: sy.source.ass_ade.test_blocked_event
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
