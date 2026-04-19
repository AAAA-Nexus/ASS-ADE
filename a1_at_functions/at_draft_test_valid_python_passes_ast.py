# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_valid_python_passes_ast.py:7
# Component id: at.source.a1_at_functions.test_valid_python_passes_ast
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_python_passes_ast(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
    result = cie.run("x = 1 + 2\n", "python")
    assert result.ast_valid is True
