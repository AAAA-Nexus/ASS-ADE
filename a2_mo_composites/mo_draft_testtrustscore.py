# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:309
# Component id: mo.source.ass_ade.testtrustscore
__version__ = "0.1.0"

class TestTrustScore:
    """Test `trust score` command — check agent trust tier and score."""

    def test_trust_score_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Trust score should return formally bounded score and tier."""
        mock_nx = MagicMock()
        mock_nx.trust_score.return_value = TrustScore(
            agent_id="agent-reliable-1",
            score=0.92,
            tier="gold",
            certified_monotonic=True,
        )
        
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["trust", "score", "agent-reliable-1", "--config", str(hybrid_config)],
            )
        
        assert result.exit_code == 0
        assert "0.92" in result.stdout or "gold" in result.stdout
