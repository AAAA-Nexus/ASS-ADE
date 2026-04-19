# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_mev_protect.py:5
# Component id: at.source.ass_ade.test_mev_protect
__version__ = "0.1.0"

def test_mev_protect(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.mev_protect.return_value = MevProtectResult(bundle_id="bun-1", protected=True, strategy="flashbots")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["mev", "protect", "0xabc,0xdef",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "bun-1" in result.stdout
