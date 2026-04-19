# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_mev_status.py:5
# Component id: at.source.ass_ade.test_mev_status
__version__ = "0.1.0"

def test_mev_status(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.mev_status.return_value = MevStatusResult(bundle_id="bun-1", status="confirmed")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["mev", "status", "bun-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "confirmed" in result.stdout
