# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_workflows.py:152
# Component id: og.source.ass_ade.test_full_certification_passes
__version__ = "0.1.0"

    def test_full_certification_passes(self) -> None:
        result = certify_output(_mock_client(), "This is a safe output.")
        assert result.passed is True
        assert result.certificate_id == "cert-123"
        assert result.lineage_id == "lin-456"
