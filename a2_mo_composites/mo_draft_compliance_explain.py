# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1064
# Component id: mo.source.ass_ade.compliance_explain
__version__ = "0.1.0"

    def compliance_explain(self, output: str, input_features: dict, **kwargs: Any) -> ExplainCert:
        """/v1/compliance/explain — GDPR Art.22 explainability cert (XPL-100). $0.040/call"""
        return self._post_model("/v1/compliance/explain", ExplainCert, {"output": output, "input_features": input_features, **kwargs})
