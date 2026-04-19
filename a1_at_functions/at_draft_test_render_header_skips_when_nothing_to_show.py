# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_render_header_skips_when_nothing_to_show.py:7
# Component id: at.source.a1_at_functions.test_render_header_skips_when_nothing_to_show
from __future__ import annotations

__version__ = "0.1.0"

def test_render_header_skips_when_nothing_to_show(self):
    from ass_ade.commands.agent import _render_phase1_header
    from io import StringIO
    from rich.console import Console as RichConsole

    agent_mock = MagicMock()
    agent_mock.last_sam_result = None
    agent_mock.last_lse_decision = None
    agent_mock.delegation_depth = 0
    agent_mock.last_cycle_report = None

    capture = StringIO()
    with patch("ass_ade.commands.agent.console", RichConsole(file=capture, force_terminal=False)):
        _render_phase1_header(agent_mock)
    # No output expected when nothing to show
    assert capture.getvalue() == ""
