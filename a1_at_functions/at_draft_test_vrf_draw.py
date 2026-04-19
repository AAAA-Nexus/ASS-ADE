# Extracted from C:/!ass-ade/tests/test_new_commands.py:881
# Component id: at.source.ass_ade.test_vrf_draw
from __future__ import annotations

__version__ = "0.1.0"

def test_vrf_draw(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.vrf_draw.return_value = VrfDraw(draw_id="draw-1", numbers=[42], proof="abc123")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["vrf", "draw", "game-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "draw-1" in result.stdout
