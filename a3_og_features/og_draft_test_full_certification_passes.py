# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_test_full_certification_passes.py:7
# Component id: og.source.a3_og_features.test_full_certification_passes
from __future__ import annotations

__version__ = "0.1.0"

def test_full_certification_passes(self) -> None:
    result = certify_output(_mock_client(), "This is a safe output.")
    assert result.passed is True
    assert result.certificate_id == "cert-123"
    assert result.lineage_id == "lin-456"
