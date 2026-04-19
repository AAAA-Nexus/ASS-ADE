# Extracted from C:/!ass-ade/tests/test_new_commands.py:822
# Component id: at.source.ass_ade.test_forge_badge
from __future__ import annotations

__version__ = "0.1.0"

def test_forge_badge(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.forge_badge.return_value = ForgeBadgeResult(badge_id="b-1", name="Gold", valid=True)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["forge", "badge", "b-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "Gold" in result.stdout
