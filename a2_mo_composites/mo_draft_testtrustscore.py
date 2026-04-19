# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testtrustscore.py:7
# Component id: mo.source.a2_mo_composites.testtrustscore
from __future__ import annotations

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
