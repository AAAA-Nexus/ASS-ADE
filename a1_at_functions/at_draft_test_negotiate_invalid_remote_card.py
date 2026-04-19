# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_negotiate_invalid_remote_card.py:7
# Component id: at.source.a1_at_functions.test_negotiate_invalid_remote_card
from __future__ import annotations

__version__ = "0.1.0"

def test_negotiate_invalid_remote_card(self, tmp_path: Path) -> None:
    mock_report = MagicMock()
    mock_report.valid = False
    mock_report.errors = [MagicMock(message="Missing name")]
    with patch("ass_ade.commands.a2a.fetch_agent_card", return_value=mock_report):
        result = runner.invoke(
            app, ["a2a", "negotiate", "https://example.com/.well-known/agent.json",
                   "--config", str(_hybrid_config(tmp_path))]
        )
    assert result.exit_code == 1
