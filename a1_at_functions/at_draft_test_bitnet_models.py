# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_bitnet_models.py:5
# Component id: at.source.ass_ade.test_bitnet_models
__version__ = "0.1.0"

def test_bitnet_models(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.bitnet_models.return_value = BitNetModelsResponse(models=[], count=0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["bitnet", "models",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
