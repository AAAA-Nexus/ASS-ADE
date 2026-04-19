# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compliance_explain.py:7
# Component id: at.source.a1_at_functions.compliance_explain
from __future__ import annotations

__version__ = "0.1.0"

def compliance_explain(self, output: str, input_features: dict, **kwargs: Any) -> ExplainCert:
    """/v1/compliance/explain — GDPR Art.22 explainability cert (XPL-100). $0.040/call"""
    return self._post_model("/v1/compliance/explain", ExplainCert, {"output": output, "input_features": input_features, **kwargs})
