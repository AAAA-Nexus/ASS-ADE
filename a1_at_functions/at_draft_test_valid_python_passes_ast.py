# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testciepipeline.py:10
# Component id: at.source.ass_ade.test_valid_python_passes_ast
__version__ = "0.1.0"

    def test_valid_python_passes_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
        result = cie.run("x = 1 + 2\n", "python")
        assert result.ast_valid is True
