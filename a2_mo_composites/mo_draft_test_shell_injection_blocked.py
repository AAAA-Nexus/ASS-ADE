# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:359
# Component id: mo.source.ass_ade.test_shell_injection_blocked
__version__ = "0.1.0"

    def test_shell_injection_blocked(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "import subprocess\nsubprocess.run('ls', shell=True)\n"
        result = cie.run(code, "python")
        assert "A03_shell_injection" in result.owasp_findings
        assert result.passed is False
