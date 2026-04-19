# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:706
# Component id: mo.source.ass_ade.security_pqc_sign
__version__ = "0.1.0"

    def security_pqc_sign(self, data: str, **kwargs: Any) -> PqcSignResult:
        """/v1/security/pqc-sign — ML-DSA (Dilithium) post-quantum signatures. $0.020/request"""
        return self._post_model("/v1/security/pqc-sign", PqcSignResult, {"data": data, **kwargs})
