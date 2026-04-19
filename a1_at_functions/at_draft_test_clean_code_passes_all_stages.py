# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_clean_code_passes_all_stages.py:7
# Component id: at.source.a1_at_functions.test_clean_code_passes_all_stages
from __future__ import annotations

__version__ = "0.1.0"

def test_clean_code_passes_all_stages(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
    code = "def add(a: int, b: int) -> int:\n    return a + b\n"
    result = cie.run(code, "python")
    assert result.ast_valid is True
    assert result.owasp_clean is True
    assert result.passed is True
