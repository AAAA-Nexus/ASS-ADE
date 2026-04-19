# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testciepipeline.py:42
# Component id: at.source.ass_ade.test_shell_injection_blocked
__version__ = "0.1.0"

    def test_shell_injection_blocked(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "import subprocess\nsubprocess.run('ls', shell=True)\n"
        result = cie.run(code, "python")
        assert "A03_shell_injection" in result.owasp_findings
        assert result.passed is False
