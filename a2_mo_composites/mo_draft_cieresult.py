# Extracted from C:/!ass-ade/src/ass_ade/agent/cie.py:51
# Component id: mo.source.ass_ade.cieresult
from __future__ import annotations

__version__ = "0.1.0"

class CIEResult:
    passed: bool
    candidate: str
    language: str
    ast_valid: bool = True
    lint_clean: bool = True
    owasp_clean: bool = True
    alphaverus_passed: bool = True
    patch_applied: bool = False
    patch_rounds: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    owasp_findings: list[str] = field(default_factory=list)
    proof_stub: str | None = None
    variant_score: float = 0.0
