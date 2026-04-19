# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:714
# Component id: mo.source.ass_ade.compliance_eu_ai_act
__version__ = "0.1.0"

    def compliance_eu_ai_act(self, system_description: str, **kwargs: Any) -> ComplianceResult:
        """/v1/compliance/eu-ai-act — Annex IV conformity certificate. $0.040/check"""
        return self._post_model("/v1/compliance/eu-ai-act", ComplianceResult, {"system_description": system_description, **kwargs})
