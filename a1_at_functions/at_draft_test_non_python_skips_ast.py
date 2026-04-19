# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_non_python_skips_ast.py:7
# Component id: at.source.a1_at_functions.test_non_python_skips_ast
from __future__ import annotations

__version__ = "0.1.0"

def test_non_python_skips_ast(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False}})
    result = cie.run("const x = 1;", "typescript")
    assert result.language == "typescript"
    # Non-python: ast_valid stays default True (no check performed)
    assert result.ast_valid is True
