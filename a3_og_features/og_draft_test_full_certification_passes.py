# Extracted from C:/!ass-ade/tests/test_workflows.py:152
# Component id: og.source.ass_ade.test_full_certification_passes
from __future__ import annotations

__version__ = "0.1.0"

def test_full_certification_passes(self) -> None:
    result = certify_output(_mock_client(), "This is a safe output.")
    assert result.passed is True
    assert result.certificate_id == "cert-123"
    assert result.lineage_id == "lin-456"
