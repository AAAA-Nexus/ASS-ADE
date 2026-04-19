# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_commands.py:187
# Component id: at.source.ass_ade.test_ratchet_advance
__version__ = "0.1.0"

def test_ratchet_advance(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.ratchet_advance.return_value = RatchetAdvance(session_id="sess-abc", new_epoch=2, proof_token="tok-xyz")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["ratchet", "advance", "sess-abc", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "new_epoch" in result.stdout
