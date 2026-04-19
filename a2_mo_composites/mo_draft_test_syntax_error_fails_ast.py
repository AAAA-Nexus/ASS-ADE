# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:333
# Component id: mo.source.ass_ade.test_syntax_error_fails_ast
__version__ = "0.1.0"

    def test_syntax_error_fails_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        result = cie.run("def foo(:\n    pass\n", "python")
        assert result.ast_valid is False
        assert result.passed is False
        assert len(result.errors) > 0
