# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testciepipeline.py:50
# Component id: at.source.ass_ade.test_clean_code_passes_all_stages
__version__ = "0.1.0"

    def test_clean_code_passes_all_stages(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
        code = "def add(a: int, b: int) -> int:\n    return a + b\n"
        result = cie.run(code, "python")
        assert result.ast_valid is True
        assert result.owasp_clean is True
        assert result.passed is True
