# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_syntax_error_fails_ast.py:7
# Component id: at.source.a1_at_functions.test_syntax_error_fails_ast
from __future__ import annotations

__version__ = "0.1.0"

def test_syntax_error_fails_ast(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False}})
    result = cie.run("def foo(:\n    pass\n", "python")
    assert result.ast_valid is False
    assert result.passed is False
    assert len(result.errors) > 0
