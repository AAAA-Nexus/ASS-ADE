# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1122
# Component id: mo.source.ass_ade.drift_certificate
__version__ = "0.1.0"

    def drift_certificate(self, check_id: str | None = None, *, model_id: str | None = None) -> DriftCertificate:
        """/v1/drift/certificate — signed drift compliance cert (DRG-101). $0.010/cert"""
        return self._get_model("/v1/drift/certificate", DriftCertificate, check_id=check_id or model_id or "")
