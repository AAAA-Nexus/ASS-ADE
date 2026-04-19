# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testciepipeline.py:59
# Component id: at.source.ass_ade.test_non_python_skips_ast
__version__ = "0.1.0"

    def test_non_python_skips_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        result = cie.run("const x = 1;", "typescript")
        assert result.language == "typescript"
        # Non-python: ast_valid stays default True (no check performed)
        assert result.ast_valid is True
