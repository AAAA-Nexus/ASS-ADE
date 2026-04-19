# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1107
# Component id: mo.source.ass_ade.drift_check
__version__ = "0.1.0"

    def drift_check(
        self,
        model_id: str,
        reference_data: dict | None = None,
        current_data: dict | None = None,
        **kwargs: Any,
    ) -> DriftCheck:
        """/v1/drift/check — PSI drift detection ≤0.20 (DRG-100). $0.010/check"""
        return self._post_model("/v1/drift/check", DriftCheck, {
            "model_id": model_id,
            "reference_data": reference_data or {},
            "current_data": current_data or {},
            **kwargs,
        })
