# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_shell_injection_blocked.py:7
# Component id: at.source.a1_at_functions.test_shell_injection_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_shell_injection_blocked(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
    code = "import subprocess\nsubprocess.run('ls', shell=True)\n"
    result = cie.run(code, "python")
    assert "A03_shell_injection" in result.owasp_findings
    assert result.passed is False
