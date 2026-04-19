# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_render_header_includes_trs_when_sam_ran.py:7
# Component id: at.source.a1_at_functions.test_render_header_includes_trs_when_sam_ran
from __future__ import annotations

__version__ = "0.1.0"

def test_render_header_includes_trs_when_sam_ran(self):
    from ass_ade.commands.agent import _render_phase1_header
    from io import StringIO
    from rich.console import Console as RichConsole

    # Patch the module's console to capture
    agent_mock = MagicMock()
    agent_mock.last_sam_result = {"composite": 0.85, "g23": True, "trs": {}}
    agent_mock.last_lse_decision = MagicMock(tier="sonnet")
    agent_mock.delegation_depth = 0
    agent_mock.last_cycle_report = None

    capture = StringIO()
    with patch("ass_ade.commands.agent.console", RichConsole(file=capture, force_terminal=False)):
        _render_phase1_header(agent_mock)
    output = capture.getvalue()
    assert "TRS=0.85" in output
    assert "LSE=sonnet" in output
