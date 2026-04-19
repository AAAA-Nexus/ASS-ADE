# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testcertifyoutput.py:12
# Component id: og.source.ass_ade.test_hallucination_failure_blocks
__version__ = "0.1.0"

    def test_hallucination_failure_blocks(self) -> None:
        client = _mock_client()
        client.hallucination_oracle.return_value = HallucinationResult(verdict="unsafe")
        result = certify_output(client, "Suspicious output that is unsafe.")
        assert result.passed is False
