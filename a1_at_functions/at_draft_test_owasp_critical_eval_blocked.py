# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testciepipeline.py:24
# Component id: at.source.ass_ade.test_owasp_critical_eval_blocked
__version__ = "0.1.0"

    def test_owasp_critical_eval_blocked(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "result = eval(user_input)\n"
        result = cie.run(code, "python")
        assert "A03_injection_eval" in result.owasp_findings
        assert result.owasp_clean is False
        assert result.passed is False
