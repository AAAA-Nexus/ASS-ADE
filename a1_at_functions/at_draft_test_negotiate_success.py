# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a_cli.py:112
# Component id: at.source.ass_ade.test_negotiate_success
__version__ = "0.1.0"

    def test_negotiate_success(self, tmp_path: Path) -> None:
        from ass_ade.a2a import A2AAgentCard, NegotiationResult
        remote_card = A2AAgentCard(
            name="RemoteAgent", description="A remote agent",
            url="https://example.com", version="1.0.0",
            skills=[], defaultInputModes=["text"], defaultOutputModes=["text"],
        )
        mock_report = MagicMock()
        mock_report.valid = True
        mock_report.card = remote_card

        neg_result = NegotiationResult(
            compatible=True, shared_skills=[], local_only=["read_file"],
            remote_only=[], auth_compatible=True, notes=[],
        )
        with patch("ass_ade.commands.a2a.fetch_agent_card", return_value=mock_report), \
             patch("ass_ade.commands.a2a.negotiate", return_value=neg_result), \
             patch("ass_ade.commands.a2a.local_agent_card", return_value=remote_card):
            result = runner.invoke(
                app, ["a2a", "negotiate", "https://example.com/.well-known/agent.json",
                       "--config", str(_hybrid_config(tmp_path))]
            )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["compatible"] is True
