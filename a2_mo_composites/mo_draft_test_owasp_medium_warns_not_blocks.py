# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:350
# Component id: mo.source.ass_ade.test_owasp_medium_warns_not_blocks
__version__ = "0.1.0"

    def test_owasp_medium_warns_not_blocks(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
        code = "import hashlib\nhashlib.md5(b'data')\n"
        result = cie.run(code, "python")
        # A02_weak_hash is medium — owasp_clean stays True, but warning present
        assert result.owasp_clean is True
        assert any("OWASP_medium" in w for w in result.warnings)
