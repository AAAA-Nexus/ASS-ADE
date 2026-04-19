# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testcertifyoutput.py:7
# Component id: og.source.a3_og_features.testcertifyoutput
from __future__ import annotations

__version__ = "0.1.0"

class TestCertifyOutput:
    def test_full_certification_passes(self) -> None:
        result = certify_output(_mock_client(), "This is a safe output.")
        assert result.passed is True
        assert result.certificate_id == "cert-123"
        assert result.lineage_id == "lin-456"

    def test_hallucination_failure_blocks(self) -> None:
        client = _mock_client()
        client.hallucination_oracle.return_value = HallucinationResult(verdict="unsafe")
        result = certify_output(client, "Suspicious output that is unsafe.")
        assert result.passed is False

    def test_empty_text_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            certify_output(_mock_client(), "")

    def test_text_preview_truncated(self) -> None:
        long_text = "A" * 200
        result = certify_output(_mock_client(), long_text)
        assert len(result.text_preview) == 120
