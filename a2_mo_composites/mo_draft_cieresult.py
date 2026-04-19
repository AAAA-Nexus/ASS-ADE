# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_cieresult.py:7
# Component id: mo.source.a2_mo_composites.cieresult
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
