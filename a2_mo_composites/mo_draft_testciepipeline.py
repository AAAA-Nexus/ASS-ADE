# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testciepipeline.py:7
# Component id: mo.source.a2_mo_composites.testciepipeline
from __future__ import annotations

__version__ = "0.1.0"

class TestCIEPipeline:
    def _make(self, **kwargs):
        from ass_ade.agent.cie import CIEPipeline
        return CIEPipeline(kwargs)

    def test_valid_python_passes_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
        result = cie.run("x = 1 + 2\n", "python")
        assert result.ast_valid is True

    def test_syntax_error_fails_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        result = cie.run("def foo(:\n    pass\n", "python")
        assert result.ast_valid is False
        assert result.passed is False
        assert len(result.errors) > 0

    def test_owasp_critical_eval_blocked(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "result = eval(user_input)\n"
        result = cie.run(code, "python")
        assert "A03_injection_eval" in result.owasp_findings
        assert result.owasp_clean is False
        assert result.passed is False

    def test_owasp_medium_warns_not_blocks(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "import hashlib\nhashlib.md5(b'data')\n"
        result = cie.run(code, "python")
        # A02_weak_hash is medium — owasp_clean stays True, but warning present
        assert result.owasp_clean is True
        assert any("OWASP_medium" in w for w in result.warnings)

    def test_shell_injection_blocked(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "import subprocess\nsubprocess.run('ls', shell=True)\n"
        result = cie.run(code, "python")
        assert "A03_shell_injection" in result.owasp_findings
        assert result.passed is False

    def test_clean_code_passes_all_stages(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "require_alphaverus": False}})
        code = "def add(a: int, b: int) -> int:\n    return a + b\n"
        result = cie.run(code, "python")
        assert result.ast_valid is True
        assert result.owasp_clean is True
        assert result.passed is True

    def test_non_python_skips_ast(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        result = cie.run("const x = 1;", "typescript")
        assert result.language == "typescript"
        # Non-python: ast_valid stays default True (no check performed)
        assert result.ast_valid is True

    def test_report_tracks_passes_failures(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        cie.run("x = 1\n", "python")
        cie.run("def bad(:\n    pass\n", "python")
        rep = cie.report()
        assert rep["passes"] >= 1
        assert rep["failures"] >= 1
        assert 0.0 <= rep["pass_rate"] <= 1.0

    def test_fail_open_on_exception(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({})
        # Should not raise even with weird input
        result = cie.run(None, "python")  # type: ignore
        assert result is not None
