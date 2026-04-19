# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1060
# Component id: mo.source.ass_ade.compliance_fairness
__version__ = "0.1.0"

    def compliance_fairness(self, dataset_description: str | None = None, *, model_id: str | None = None, **kwargs: Any) -> FairnessProof:
        """/v1/compliance/fairness — disparate impact ratio (FNS-100). $0.040/check"""
        return self._post_model("/v1/compliance/fairness", FairnessProof, {"dataset_description": dataset_description or model_id or "", **kwargs})
