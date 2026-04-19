# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_forge_verify.py:5
# Component id: at.source.ass_ade.test_forge_verify
__version__ = "0.1.0"

def test_forge_verify(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.forge_verify.return_value = ForgeVerifyResult(verified=True, agent_id="agent-1", score=0.98, badge_awarded="gold")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["forge", "verify", "agent-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "True" in result.stdout
