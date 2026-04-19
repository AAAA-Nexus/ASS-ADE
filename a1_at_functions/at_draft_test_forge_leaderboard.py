# Extracted from C:/!ass-ade/tests/test_new_commands.py:794
# Component id: at.source.ass_ade.test_forge_leaderboard
from __future__ import annotations

__version__ = "0.1.0"

def test_forge_leaderboard(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.forge_leaderboard.return_value = ForgeLeaderboardResponse(entries=[], epoch=42)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["forge", "leaderboard",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
